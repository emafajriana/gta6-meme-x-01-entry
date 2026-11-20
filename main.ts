// Entry runner for the make.fun bounty "gta6-meme-x-01".
//
// Challenger entry: the meme is a Steam purchase receipt dated
// September 17, 2013 for a GTA VI pre-order that is still
// "Preparing to ship", estimated delivery November 19, 2026.
//
// The whole job is deliberately tiny: hand the grader the post address by
// copying POST.json from this repository into the output directory. The
// meme itself lives on X; this program only delivers its address.
//
// Locations can be overridden for local runs:
//   MAKEFUN_BOT_DIR    where POST.json is read from (default "/bot")
//   MAKEFUN_OUTPUT_DIR where POST.json is written to (default "/output")
//
// Success is silent. Any failure explains itself on stderr and exits 1.

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const botDir: string = process.env.MAKEFUN_BOT_DIR?.trim() || "/bot";
const outputDir: string = process.env.MAKEFUN_OUTPUT_DIR?.trim() || "/output";

const sourcePath: string = join(botDir, "POST.json");
const targetPath: string = join(outputDir, "POST.json");

try {
  mkdirSync(outputDir, { recursive: true });
  copyFileSync(sourcePath, targetPath);
} catch (err) {
  const detail = err instanceof Error ? err.message : String(err);
  console.error(`main.ts: failed to copy POST.json (${sourcePath} -> ${targetPath}): ${detail}`);
  process.exit(1);
}
