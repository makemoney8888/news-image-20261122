import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// The competition gate: a PNG (or JPEG) of at most 1 MiB and at most
// 1024 x 1024 pixels. This entry is a PNG, so verify the signature, the
// IHDR dimensions and the size cap before copying it out.
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1_048_576;
const MAX_DIMENSION = 1024;

function fail(message: string): never {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

if (!existsSync(source)) {
  fail(`entry.png not found next to main.ts: ${source}`);
}

const bytes = readFileSync(source);
if (bytes.length < 8 || !bytes.subarray(0, 8).equals(PNG_SIGNATURE)) {
  fail("entry.png is missing a valid PNG signature; refusing to copy it.");
}
if (bytes.length > MAX_BYTES) {
  fail(`entry.png is ${bytes.length} bytes, over the 1 MiB limit.`);
}
// IHDR chunk: width at bytes 16-19, height at bytes 20-23 (big-endian).
if (bytes.length < 24 || bytes.toString("ascii", 12, 16) !== "IHDR") {
  fail("entry.png has no IHDR chunk where one is expected.");
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > MAX_DIMENSION || height > MAX_DIMENSION) {
  fail(`entry.png is ${width}x${height}, over the 1024x1024 limit.`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
console.log(`Wrote ${target} (${bytes.length} bytes, ${width}x${height})`);
