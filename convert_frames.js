const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

async function convertFrames(inputDir, quality) {
    const files = fs.readdirSync(inputDir)
        .filter(f => f.endsWith('.png'))
        .sort();

    console.log(`Converting ${files.length} PNG frames in ${inputDir} to WebP (quality ${quality})...`);

    let totalPngSize = 0;
    let totalWebpSize = 0;
    let converted = 0;

    for (const file of files) {
        const inputPath = path.join(inputDir, file);
        const outputPath = path.join(inputDir, file.replace('.png', '.webp'));

        const pngSize = fs.statSync(inputPath).size;
        totalPngSize += pngSize;

        // Skip if already converted with valid output
        if (fs.existsSync(outputPath)) {
            const webpStat = fs.statSync(outputPath);
            if (webpStat.size > 0) {
                totalWebpSize += webpStat.size;
                converted++;
                continue;
            }
        }

        try {
            await sharp(inputPath)
                .webp({ quality: quality })
                .toFile(outputPath);

            const webpSize = fs.statSync(outputPath).size;
            totalWebpSize += webpSize;
            converted++;

            if (converted % 20 === 0) {
                process.stdout.write(`  Converted ${converted}/${files.length}...\r`);
            }
        } catch (err) {
            console.error(`  Error converting ${file}:`, err.message);
        }
    }

    console.log(`Done! Converted ${converted}/${files.length} frames.`);
    console.log(`  PNG total: ${(totalPngSize / 1024 / 1024).toFixed(1)} MB`);
    console.log(`  WebP total: ${(totalWebpSize / 1024 / 1024).toFixed(1)} MB`);
    console.log(`  Savings: ${((1 - totalWebpSize / totalPngSize) * 100).toFixed(1)}%`);
}

async function main() {
    const rootDir = path.resolve(__dirname);

    console.log('=== HERO DESKTOP FRAMES ===');
    await convertFrames(path.join(rootDir, 'assets/frames/hero_desktop'), 80);

    console.log('\n=== HERO MOBILE FRAMES ===');
    await convertFrames(path.join(rootDir, 'assets/frames/hero_mobile'), 80);
}

main().catch(console.error);
