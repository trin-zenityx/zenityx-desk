// ZenityX Desk — self-hosted update feed (RustDesk-compatible version check).
// The client POSTs {os, os_version, arch, device_id, typ} and expects a JSON
// body {"url": "..."} whose LAST path segment is the latest version string.
// The client shows an update prompt only when that version > the installed one.
//
// To PUSH an update later: bump LATEST to the new version AND make the url point
// at the real installer/download for that version.
const LATEST = "1.4.6"; // == currently shipped build → no false "update available" prompt

export async function onRequest() {
  return new Response(
    JSON.stringify({ url: `https://desk.zenityx.com/download/${LATEST}` }),
    {
      headers: {
        "content-type": "application/json; charset=utf-8",
        "cache-control": "no-store",
      },
    },
  );
}
