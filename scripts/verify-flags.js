const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml'); // Assuming js-yaml is available or will be in requirements.txt

/**
 * verify-flags.js
 * Scans source code for feature flag usage and compares against config.
 */

function scanDir(dir, fileList = []) {
    const files = fs.readdirSync(dir);
    files.forEach(file => {
        const filePath = path.join(dir, file);
        if (fs.statSync(filePath).isDirectory()) {
            if (!['node_modules', '.git', 'dist', 'build'].includes(file)) {
                scanDir(filePath, fileList);
            }
        } else if (/\.(js|ts|jsx|tsx|py)$/.test(file)) {
            fileList.push(filePath);
        }
    });
    return fileList;
}

function extractFlags(files) {
    const flagsFound = new Set();
    const flagRegex = /isEnabled\(['"]([^'"]+)['"]|is_enabled\(['"]([^'"]+)['"]|check\(['"]([^'"]+)['"]/g;

    files.forEach(file => {
        const content = fs.readFileSync(file, 'utf8');
        let match;
        while ((match = flagRegex.exec(content)) !== null) {
            const flag = match[1] || match[2] || match[3];
            if (flag) flagsFound.add(flag);
        }
    });
    return Array.from(flagsFound);
}

function verifyFlags(sourcePath, configPath) {
    if (!fs.existsSync(configPath)) {
        console.error(`\x1b[31m[Error]\x1b[0m Config file not found: ${configPath}`);
        process.exit(1);
    }

    let config;
    try {
        const configContent = fs.readFileSync(configPath, 'utf8');
        config = configPath.endsWith('.yml') || configPath.endsWith('.yaml')
            ? yaml.load(configContent)
            : JSON.parse(configContent);
    } catch (e) {
        console.error(`\x1b[31m[Error]\x1b[0m Failed to parse config: ${e.message}`);
        process.exit(1);
    }

    const configFlags = Object.keys(config);
    const sourceFiles = scanDir(sourcePath);
    const usedFlags = extractFlags(sourceFiles);

    console.log(`\n\x1b[34m[Verification]\x1b[0m Scanning ${sourceFiles.length} files for flags...`);

    const missingInConfig = usedFlags.filter(f => !configFlags.includes(f));
    const unusedInSource = configFlags.filter(f => !usedFlags.includes(f));

    if (missingInConfig.length > 0) {
        console.log(`\x1b[33m[Warning]\x1b[0m Flags used in code but missing from config:`);
        missingInConfig.forEach(f => console.log(`  - ${f}`));
    }

    if (unusedInSource.length > 0) {
        console.log(`\x1b[36m[Note]\x1b[0m Flags defined in config but not found in source:`);
        unusedInSource.forEach(f => console.log(`  - ${f}`));
    }

    if (missingInConfig.length === 0) {
        console.log(`\x1b[32m[Pass]\x1b[0m All flags used in source are defined in config.\n`);
    } else {
        process.exit(1);
    }
}

// Simple CLI handling
const args = process.argv.slice(2);
const sourceArg = args.find(a => a.startsWith('--path='))?.split('=')[1] || './src';
const configArg = args.find(a => a.startsWith('--config='))?.split('=')[1] || './feature-flags.yml';

verifyFlags(sourceArg, configArg);
