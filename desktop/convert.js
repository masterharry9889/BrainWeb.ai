const sharp = require('sharp');
const pngToIco = require('png-to-ico');
const fs = require('fs');

async function convert() {
  const input = '../frontend/logo/21b08db87f66fdbe20e5f52fa9ddb93f.webp';
  const pngTemp = 'temp_icon.png';
  const icoOut = 'icon.ico';

  try {
    // 1. Convert WebP to PNG using Sharp
    await sharp(input)
      .resize(256, 256)
      .png()
      .toFile(pngTemp);
    console.log('PNG created.');

    // 2. Convert PNG to ICO
    const buf = await pngToIco(pngTemp);
    fs.writeFileSync(icoOut, buf);
    console.log('ICO created successfully.');

    // 3. Clean up
    fs.unlinkSync(pngTemp);
  } catch (err) {
    console.error('Error:', err);
  }
}

convert();
