import fs from "fs";
import path from "path";

if (process.argv.length <= 2) {
  console.log(`Usage: node ./sort-txt.mjs path/to/cj3.txt`);
}

function block(ch) {
  const cp = ch.codePointAt(0);
  if (cp <= 0x4dbf && cp >= 0x3400) {
    return 1; // Ext. A
  } else if (cp <= 0xffff) {
    return 0; // Basic + Misc
  } else if (cp <= 0x2a6df) {
    return 2;
  } else if (cp <= 0x2b73f) {
    return 3;
  } else if (cp <= 0x2b81f) {
    return 3; // Ext. C & Ext. D are mixed :(
  } else if (cp <= 0x2ceaf) {
    return 5;
  } else if (cp <= 0x2ebef) {
    return 6;
  } else if (cp <= 0x3134f) {
    return 7;
  } else {
    throw new Error(`Unsupported character: U+${cp.toString(16)} ${ch}`);
  }
}
function sign(x, y) {
  if (x < y) {
    return -1;
  }
  if (x > y) {
    return 1;
  }
  return 0;
}

function compare(cj1, cj2, ch1, ch2) {
  const c = sign(block(ch1), block(ch2));
  if (c !== 0) {
    // sort by different blocks
    return c;
  } else {
    if (block(ch1) === 0 && block(ch2) === 0) {
      return 0; // do not sort BMP, which is manually sorted.
    }
    return sign(cj1, cj2);
  }
}

function sortTxt(text) {
  const [prefaces, items] = text.split("[DATA]\r\n");
  const lines = items.split("\r\n");
  lines.sort((l1, l2) => {
    if (!l1 || !l2) {
      return 0;
    }
    const CJMatchers = /^(?<cjcode>[a-z]+)\s+(?<character>.)/u;
    try {
      const { cjcode: cj1, character: ch1 } = CJMatchers.exec(l1).groups;
      const { cjcode: cj2, character: ch2 } = CJMatchers.exec(l2).groups;
      return compare(cj1, cj2, ch1, ch2);
    } catch (e) {
      console.error(e);
      console.log(l1, l2);
    }
  });
  return prefaces + "[DATA]\r\n" + lines.join("\r\n");
}

const txtPath = path.resolve(process.argv[2]);

fs.writeFileSync(
  txtPath,
  sortTxt(fs.readFileSync(txtPath, { encoding: "utf-8" }))
);
