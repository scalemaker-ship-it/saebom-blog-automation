import Vision
import AppKit
func ear(_ r: VNFaceLandmarkRegion2D?) -> Double {
  guard let r = r, r.pointCount > 0 else { return -1 }
  let p = r.normalizedPoints
  let xs = p.map{Double($0.x)}, ys = p.map{Double($0.y)}
  let w = xs.max()! - xs.min()!, h = ys.max()! - ys.min()!
  return w > 0 ? h / w : -1
}
for path in CommandLine.arguments.dropFirst() {
  let img = NSImage(contentsOfFile: path)!
  var r = CGRect(origin: .zero, size: img.size)
  let cg = img.cgImage(forProposedRect: &r, context: nil, hints: nil)!
  let req = VNDetectFaceLandmarksRequest()
  try! VNImageRequestHandler(cgImage: cg, options: [:]).perform([req])
  let W = Double(cg.width), H = Double(cg.height)
  var out: [String] = []
  for o in req.results ?? [] {
    let b = o.boundingBox
    let l = ear(o.landmarks?.leftEye), rr = ear(o.landmarks?.rightEye)
    out.append(String(format: "box=%d,%d,%d,%d L=%.2f R=%.2f", Int(b.minX*W), Int((1-b.maxY)*H), Int(b.width*W), Int(b.height*H), l, rr))
  }
  print("\((path as NSString).lastPathComponent) | \(out.joined(separator: " ; "))")
}
