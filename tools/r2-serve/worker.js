// UI media-serve worker — GET public media, PUT uploads gated by env.UPLOAD_KEY.
// Clean-room port of the CHM `tools/r2-serve` pattern (see docs/PROVENANCE.md)
// with the historical hardcoded-secret defect removed: the upload key is a
// Wrangler secret (`wrangler secret put UPLOAD_KEY`), never in source.
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const key = url.pathname.replace(/^\//, "");
    if (request.method === "PUT") {
      if (!env.UPLOAD_KEY || request.headers.get("x-upload-key") !== env.UPLOAD_KEY) {
        return new Response("forbidden", { status: 403 });
      }
      if (!key) return new Response("missing key", { status: 400 });
      await env.UI_MEDIA.put(key, request.body, {
        httpMetadata: { contentType: request.headers.get("content-type") || "application/octet-stream" },
      });
      return new Response("ok", { status: 201 });
    }
    const obj = await env.UI_MEDIA.get(key);
    if (!obj) return new Response("not found", { status: 404 });
    const headers = new Headers();
    obj.writeHttpMetadata(headers);
    headers.set("Cache-Control", "public, max-age=3600");
    return new Response(obj.body, { headers });
  },
};
