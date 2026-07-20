import Foundation
import AVFoundation
import CoreGraphics
import CoreImage
import CoreMedia
import CoreVideo
import ImageIO
import UniformTypeIdentifiers

enum EncodeError: Error, CustomStringConvertible {
    case usage
    case noFrames
    case invalidArgument(String)
    case cannotCreateWriter
    case cannotAddInput
    case cannotCreatePixelBufferPool
    case cannotCreatePixelBuffer(Int)
    case cannotReadImage(String)
    case appendFailed(Int)
    case writerFailed(String)
    case thumbnailFailed

    var description: String {
        switch self {
        case .usage:
            return "Usage: encode_avfoundation <frames_dir> <output_mp4> <thumbnail_jpg> [width] [height] [fps] [bitrate]"
        case .noFrames: return "No JPEG or PNG frames found"
        case .invalidArgument(let value): return "Invalid positive integer: \(value)"
        case .cannotCreateWriter: return "Could not create AVAssetWriter"
        case .cannotAddInput: return "Could not add video input"
        case .cannotCreatePixelBufferPool: return "Could not create pixel buffer pool"
        case .cannotCreatePixelBuffer(let index): return "Could not create pixel buffer for frame \(index)"
        case .cannotReadImage(let path): return "Could not read image: \(path)"
        case .appendFailed(let index): return "Failed to append frame \(index)"
        case .writerFailed(let message): return "Writer failed: \(message)"
        case .thumbnailFailed: return "Video encoded, but thumbnail extraction failed"
        }
    }
}

func positiveInt(_ args: [String], _ index: Int, _ fallback: Int) throws -> Int {
    guard index < args.count else { return fallback }
    guard let value = Int(args[index]), value > 0 else {
        throw EncodeError.invalidArgument(args[index])
    }
    return value
}

func imageFiles(in directory: URL) throws -> [URL] {
    return try FileManager.default
        .contentsOfDirectory(at: directory, includingPropertiesForKeys: [.isRegularFileKey])
        .filter { ["jpg", "jpeg", "png"].contains($0.pathExtension.lowercased()) }
        .sorted { $0.lastPathComponent.localizedStandardCompare($1.lastPathComponent) == .orderedAscending }
}

func loadCGImage(_ url: URL) -> CGImage? {
    guard let source = CGImageSourceCreateWithURL(url as CFURL, nil) else { return nil }
    return CGImageSourceCreateImageAtIndex(source, 0, nil)
}

func makePixelBuffer(from image: CGImage, pool: CVPixelBufferPool, width: Int, height: Int, index: Int) throws -> CVPixelBuffer {
    var optionalBuffer: CVPixelBuffer?
    guard CVPixelBufferPoolCreatePixelBuffer(nil, pool, &optionalBuffer) == kCVReturnSuccess,
          let buffer = optionalBuffer else { throw EncodeError.cannotCreatePixelBuffer(index) }
    CVPixelBufferLockBaseAddress(buffer, [])
    defer { CVPixelBufferUnlockBaseAddress(buffer, []) }
    guard let baseAddress = CVPixelBufferGetBaseAddress(buffer),
          let context = CGContext(
            data: baseAddress,
            width: width,
            height: height,
            bitsPerComponent: 8,
            bytesPerRow: CVPixelBufferGetBytesPerRow(buffer),
            space: CGColorSpaceCreateDeviceRGB(),
            bitmapInfo: CGBitmapInfo.byteOrder32Little.rawValue | CGImageAlphaInfo.premultipliedFirst.rawValue
          ) else { throw EncodeError.cannotCreatePixelBuffer(index) }
    context.setFillColor(CGColor(gray: 0, alpha: 1))
    context.fill(CGRect(x: 0, y: 0, width: width, height: height))
    context.interpolationQuality = .high
    context.draw(image, in: CGRect(x: 0, y: 0, width: width, height: height))
    return buffer
}

func encode(framesDirectory: URL, outputURL: URL, width: Int, height: Int, fps: Int32, bitrate: Int) throws -> Int {
    let frames = try imageFiles(in: framesDirectory)
    guard !frames.isEmpty else { throw EncodeError.noFrames }
    try? FileManager.default.removeItem(at: outputURL)
    guard let writer = try? AVAssetWriter(outputURL: outputURL, fileType: .mp4) else {
        throw EncodeError.cannotCreateWriter
    }
    let settings: [String: Any] = [
        AVVideoCodecKey: AVVideoCodecType.h264,
        AVVideoWidthKey: width,
        AVVideoHeightKey: height,
        AVVideoCompressionPropertiesKey: [
            AVVideoAverageBitRateKey: bitrate,
            AVVideoExpectedSourceFrameRateKey: Int(fps),
            AVVideoMaxKeyFrameIntervalKey: Int(fps) * 2,
            AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel
        ]
    ]
    let input = AVAssetWriterInput(mediaType: .video, outputSettings: settings)
    input.expectsMediaDataInRealTime = false
    let adaptor = AVAssetWriterInputPixelBufferAdaptor(
        assetWriterInput: input,
        sourcePixelBufferAttributes: [
            kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA,
            kCVPixelBufferWidthKey as String: width,
            kCVPixelBufferHeightKey as String: height,
            kCVPixelBufferIOSurfacePropertiesKey as String: [:]
        ]
    )
    guard writer.canAdd(input) else { throw EncodeError.cannotAddInput }
    writer.add(input)
    guard writer.startWriting() else {
        throw EncodeError.writerFailed(writer.error?.localizedDescription ?? "unknown start error")
    }
    writer.startSession(atSourceTime: .zero)
    guard let pool = adaptor.pixelBufferPool else { throw EncodeError.cannotCreatePixelBufferPool }

    for (offset, frameURL) in frames.enumerated() {
        while !input.isReadyForMoreMediaData {
            Thread.sleep(forTimeInterval: 0.002)
            if writer.status == .failed {
                throw EncodeError.writerFailed(writer.error?.localizedDescription ?? "unknown error")
            }
        }
        guard let image = loadCGImage(frameURL) else { throw EncodeError.cannotReadImage(frameURL.path) }
        let buffer = try makePixelBuffer(from: image, pool: pool, width: width, height: height, index: offset + 1)
        guard adaptor.append(buffer, withPresentationTime: CMTime(value: CMTimeValue(offset), timescale: fps)) else {
            throw EncodeError.appendFailed(offset + 1)
        }
        if (offset + 1) % 150 == 0 || offset + 1 == frames.count {
            print("encoded \(offset + 1)/\(frames.count)")
            fflush(stdout)
        }
    }
    input.markAsFinished()
    let semaphore = DispatchSemaphore(value: 0)
    writer.finishWriting { semaphore.signal() }
    semaphore.wait()
    guard writer.status == .completed else {
        throw EncodeError.writerFailed(writer.error?.localizedDescription ?? "unknown finish error")
    }
    return frames.count
}

func createThumbnail(videoURL: URL, outputURL: URL, seconds: Double) async throws {
    try? FileManager.default.removeItem(at: outputURL)
    let generator = AVAssetImageGenerator(asset: AVURLAsset(url: videoURL))
    generator.appliesPreferredTrackTransform = true
    let result = try await generator.image(at: CMTime(seconds: seconds, preferredTimescale: 600))
    guard let destination = CGImageDestinationCreateWithURL(outputURL as CFURL, UTType.jpeg.identifier as CFString, 1, nil)
    else { throw EncodeError.thumbnailFailed }
    CGImageDestinationAddImage(destination, result.image, [kCGImageDestinationLossyCompressionQuality: 0.9] as CFDictionary)
    guard CGImageDestinationFinalize(destination) else { throw EncodeError.thumbnailFailed }
}

let args = CommandLine.arguments
guard args.count >= 4 && args.count <= 8 else {
    fputs("\(EncodeError.usage)\n", stderr)
    exit(2)
}

do {
    let width = try positiveInt(args, 4, 1080)
    let height = try positiveInt(args, 5, 1920)
    let fps = try positiveInt(args, 6, 30)
    let bitrate = try positiveInt(args, 7, 12_000_000)
    let framesDirectory = URL(fileURLWithPath: args[1], isDirectory: true)
    let outputURL = URL(fileURLWithPath: args[2])
    let thumbnailURL = URL(fileURLWithPath: args[3])
    let started = Date()
    let count = try encode(
        framesDirectory: framesDirectory,
        outputURL: outputURL,
        width: width,
        height: height,
        fps: Int32(fps),
        bitrate: bitrate
    )
    let semaphore = DispatchSemaphore(value: 0)
    var thumbnailError: Error?
    Task {
        do {
            try await createThumbnail(
                videoURL: outputURL,
                outputURL: thumbnailURL,
                seconds: max(0, Double(count) / Double(fps) / 2)
            )
        } catch { thumbnailError = error }
        semaphore.signal()
    }
    semaphore.wait()
    if let thumbnailError { throw thumbnailError }
    print("complete frames=\(count) elapsed_seconds=\(String(format: "%.2f", Date().timeIntervalSince(started))) output=\(outputURL.path)")
} catch {
    fputs("error: \(error)\n", stderr)
    exit(1)
}
