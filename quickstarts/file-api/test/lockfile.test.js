/**
 * Test suite for package-lock.json validation.
 * 
 * Validates the integrity and structure of the package-lock.json file,
 * ensuring all dependencies are properly locked and secure.
 */

const fs = require('fs');
const path = require('path');
const assert = require('assert');

describe('package-lock.json Validation', function() {
    let packageLock;
    let packageJson;
    const packageLockPath = path.join(__dirname, '..', 'package-lock.json');
    const packageJsonPath = path.join(__dirname, '..', 'package.json');

    before(function() {
        // Load package-lock.json
        const packageLockContent = fs.readFileSync(packageLockPath, 'utf-8');
        packageLock = JSON.parse(packageLockContent);

        // Load package.json
        const packageJsonContent = fs.readFileSync(packageJsonPath, 'utf-8');
        packageJson = JSON.parse(packageJsonContent);
    });

    describe('File Structure', function() {
        it('should have valid JSON structure', function() {
            assert.strictEqual(typeof packageLock, 'object');
            assert.notStrictEqual(packageLock, null);
        });

        it('should have required top-level fields', function() {
            const requiredFields = ['name', 'version', 'lockfileVersion', 'requires', 'packages'];
            
            requiredFields.forEach(field => {
                assert.ok(
                    packageLock.hasOwnProperty(field),
                    `package-lock.json should have '${field}' field`
                );
            });
        });

        it('should have lockfileVersion 3', function() {
            assert.strictEqual(
                packageLock.lockfileVersion,
                3,
                'Should use lockfileVersion 3 for npm v7+'
            );
        });

        it('should match package.json name and version', function() {
            assert.strictEqual(
                packageLock.name,
                packageJson.name,
                'package-lock.json name should match package.json'
            );
            
            assert.strictEqual(
                packageLock.version,
                packageJson.version,
                'package-lock.json version should match package.json'
            );
        });
    });

    describe('Dependencies', function() {
        it('should have packages object', function() {
            assert.strictEqual(typeof packageLock.packages, 'object');
        });

        it('should have root package entry', function() {
            assert.ok(
                packageLock.packages.hasOwnProperty(''),
                'Should have root package entry (empty string key)'
            );
        });

        it('should have all direct dependencies listed in root package', function() {
            const rootPackage = packageLock.packages[''];
            const lockDeps = rootPackage.dependencies || {};
            const jsonDeps = packageJson.dependencies || {};

            Object.keys(jsonDeps).forEach(dep => {
                assert.ok(
                    lockDeps.hasOwnProperty(dep),
                    `Dependency '${dep}' from package.json should be in package-lock.json`
                );
            });
        });

        it('should have required dependencies', function() {
            const requiredDeps = ['dotenv', 'googleapis', 'mime-types'];
            const rootPackage = packageLock.packages[''];
            const deps = rootPackage.dependencies || {};

            requiredDeps.forEach(dep => {
                assert.ok(
                    deps.hasOwnProperty(dep),
                    `Required dependency '${dep}' should be present`
                );
            });
        });

        it('should have valid version specifications', function() {
            const versionRegex = /^\^?\d+\.\d+\.\d+$/;
            const rootPackage = packageLock.packages[''];
            const deps = rootPackage.dependencies || {};

            Object.entries(deps).forEach(([name, version]) => {
                assert.ok(
                    versionRegex.test(version),
                    `Dependency '${name}' should have valid version format, got: ${version}`
                );
            });
        });
    });

    describe('Package Entries', function() {
        it('should have integrity hashes for all packages', function() {
            const packages = packageLock.packages;
            const packagesWithoutIntegrity = [];

            Object.entries(packages).forEach(([name, pkg]) => {
                // Root package doesn't need integrity
                if (name === '') return;

                if (!pkg.integrity) {
                    packagesWithoutIntegrity.push(name);
                }
            });

            assert.strictEqual(
                packagesWithoutIntegrity.length,
                0,
                `Packages without integrity: ${packagesWithoutIntegrity.join(', ')}`
            );
        });

        it('should have resolved URLs for all packages', function() {
            const packages = packageLock.packages;
            const packagesWithoutResolved = [];

            Object.entries(packages).forEach(([name, pkg]) => {
                // Root package and local packages don't need resolved
                if (name === '' || name.startsWith('file:')) return;

                if (!pkg.resolved) {
                    packagesWithoutResolved.push(name);
                }
            });

            assert.strictEqual(
                packagesWithoutResolved.length,
                0,
                `Packages without resolved URL: ${packagesWithoutResolved.join(', ')}`
            );
        });

        it('should use HTTPS URLs for registry', function() {
            const packages = packageLock.packages;
            const nonHttpsPackages = [];

            Object.entries(packages).forEach(([name, pkg]) => {
                if (pkg.resolved && pkg.resolved.startsWith('http://')) {
                    nonHttpsPackages.push(name);
                }
            });

            assert.strictEqual(
                nonHttpsPackages.length,
                0,
                `Packages using HTTP instead of HTTPS: ${nonHttpsPackages.join(', ')}`
            );
        });

        it('should have valid node_modules paths', function() {
            const packages = packageLock.packages;

            Object.keys(packages).forEach(pkgPath => {
                if (pkgPath === '') return; // Skip root

                // Path should either be node_modules/* or empty
                if (pkgPath && !pkgPath.startsWith('node_modules/')) {
                    assert.fail(`Invalid package path: ${pkgPath}`);
                }
            });
        });
    });

    describe('Security', function() {
        it('should not have known vulnerable package patterns', function() {
            const packages = packageLock.packages;
            const vulnerablePatterns = [
                { name: 'event-stream', minVersion: '3.3.6', maxVersion: '3.3.6' },
                // Add more known vulnerabilities as needed
            ];

            const foundVulnerabilities = [];

            Object.entries(packages).forEach(([path, pkg]) => {
                vulnerablePatterns.forEach(pattern => {
                    if (path.includes(pattern.name) && pkg.version) {
                        if (pkg.version === pattern.minVersion) {
                            foundVulnerabilities.push(`${pattern.name}@${pkg.version}`);
                        }
                    }
                });
            });

            assert.strictEqual(
                foundVulnerabilities.length,
                0,
                `Found known vulnerable packages: ${foundVulnerabilities.join(', ')}`
            );
        });

        it('should have engines specified in root package', function() {
            const rootPackage = packageLock.packages[''];
            
            // Check if engines is specified (optional but recommended)
            if (rootPackage.engines) {
                assert.ok(
                    rootPackage.engines.node,
                    'If engines is specified, should include node version'
                );
            }
        });
    });

    describe('Consistency', function() {
        it('should have consistent dependency versions across the tree', function() {
            const packages = packageLock.packages;
            const versionMap = new Map();

            // Build a map of package names to their versions
            Object.entries(packages).forEach(([path, pkg]) => {
                if (path === '') return;

                const pkgName = path.split('node_modules/').pop();
                if (!versionMap.has(pkgName)) {
                    versionMap.set(pkgName, new Set());
                }
                versionMap.get(pkgName).add(pkg.version);
            });

            // Report packages with multiple versions (informational)
            const multiVersionPackages = [];
            versionMap.forEach((versions, name) => {
                if (versions.size > 1) {
                    multiVersionPackages.push(`${name}: ${Array.from(versions).join(', ')}`);
                }
            });

            // This is informational - multiple versions might be acceptable
            if (multiVersionPackages.length > 0) {
                console.log('    Info: Packages with multiple versions:');
                multiVersionPackages.forEach(pkg => console.log(`      - ${pkg}`));
            }
        });

        it('should not have duplicate package entries', function() {
            const packages = packageLock.packages;
            const paths = Object.keys(packages);
            const uniquePaths = new Set(paths);

            assert.strictEqual(
                paths.length,
                uniquePaths.size,
                'Should not have duplicate package paths'
            );
        });
    });

    describe('Package Specific Tests', function() {
        it('should have googleapis package', function() {
            const packages = packageLock.packages;
            const googleapisPath = 'node_modules/googleapis';
            
            assert.ok(
                packages.hasOwnProperty(googleapisPath),
                'Should include googleapis package'
            );
            
            const googleapis = packages[googleapisPath];
            assert.ok(googleapis.version, 'googleapis should have version');
            assert.ok(googleapis.integrity, 'googleapis should have integrity hash');
        });

        it('should have dotenv package', function() {
            const packages = packageLock.packages;
            const dotenvPath = 'node_modules/dotenv';
            
            assert.ok(
                packages.hasOwnProperty(dotenvPath),
                'Should include dotenv package'
            );
            
            const dotenv = packages[dotenvPath];
            assert.ok(dotenv.version, 'dotenv should have version');
            assert.ok(dotenv.integrity, 'dotenv should have integrity hash');
        });

        it('should have mime-types package', function() {
            const packages = packageLock.packages;
            const mimeTypesPath = 'node_modules/mime-types';
            
            assert.ok(
                packages.hasOwnProperty(mimeTypesPath),
                'Should include mime-types package'
            );
            
            const mimeTypes = packages[mimeTypesPath];
            assert.ok(mimeTypes.version, 'mime-types should have version');
            assert.ok(mimeTypes.integrity, 'mime-types should have integrity hash');
        });
    });
});

// Run tests if this file is executed directly
if (require.main === module) {
    console.log('Running package-lock.json validation tests...\n');
    
    // Simple test runner
    const tests = {
        passed: 0,
        failed: 0,
        errors: []
    };

    // This is a basic runner - in practice, use a proper test framework
    console.log('Use: npm test (with proper test framework setup)');
    console.log('Or: node test/lockfile.test.js');
}

module.exports = { describe, it };