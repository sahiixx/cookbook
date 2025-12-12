/**
 * Tests for quickstarts/file-api/sample.js
 * Validates the File API sample code functionality
 */

const fs = require('fs');
const path = require('path');

// Mock dependencies
jest.mock('dotenv');
jest.mock('fs');
jest.mock('googleapis');
jest.mock('mime-types');

describe('File API Sample', () => {
  let sampleCode;
  
  beforeAll(() => {
    // Read the sample.js file
    const samplePath = path.join(__dirname, '../../quickstarts/file-api/sample.js');
    sampleCode = fs.readFileSync(samplePath, 'utf-8');
  });
  
  describe('File Structure', () => {
    test('sample.js file exists', () => {
      const samplePath = path.join(__dirname, '../../quickstarts/file-api/sample.js');
      expect(fs.existsSync(samplePath)).toBe(true);
    });
    
    test('file is not empty', () => {
      expect(sampleCode.length).toBeGreaterThan(0);
    });
  });
  
  describe('Copyright and License', () => {
    test('contains copyright notice', () => {
      expect(sampleCode).toMatch(/Copyright 2025 Google LLC/);
    });
    
    test('contains Apache 2.0 license', () => {
      expect(sampleCode).toMatch(/Apache License, Version 2.0/);
    });
    
    test('contains license URL', () => {
      expect(sampleCode).toMatch(/https:\/\/www\.apache\.org\/licenses\/LICENSE-2\.0/);
    });
  });
  
  describe('Dependencies', () => {
    test('requires dotenv', () => {
      expect(sampleCode).toMatch(/require\(['"]dotenv['"]\)/);
    });
    
    test('requires fs', () => {
      expect(sampleCode).toMatch(/require\(['"]fs['"]\)/);
    });
    
    test('requires googleapis', () => {
      expect(sampleCode).toMatch(/require\(['"]googleapis['"]\)/);
    });
    
    test('requires mime-types', () => {
      expect(sampleCode).toMatch(/require\(['"]mime-types['"]\)/);
    });
  });
  
  describe('Environment Configuration', () => {
    test('loads environment variables from .env file', () => {
      expect(sampleCode).toMatch(/dotenv\.config/);
      expect(sampleCode).toMatch(/path:\s*['"]\.env['"]/);
    });
    
    test('reads GOOGLE_API_KEY from environment', () => {
      expect(sampleCode).toMatch(/process\.env\.GOOGLE_API_KEY/);
    });
    
    test('constructs GENAI_DISCOVERY_URL', () => {
      expect(sampleCode).toMatch(/GENAI_DISCOVERY_URL/);
      expect(sampleCode).toMatch(/generativelanguage\.googleapis\.com/);
      expect(sampleCode).toMatch(/version=v1beta/);
    });
  });
  
  describe('API Client Initialization', () => {
    test('initializes genaiService using discoverAPI', () => {
      expect(sampleCode).toMatch(/google\.discoverAPI/);
      expect(sampleCode).toMatch(/url:\s*GENAI_DISCOVERY_URL/);
    });
    
    test('creates GoogleAuth instance', () => {
      expect(sampleCode).toMatch(/google\.auth\.GoogleAuth/);
      expect(sampleCode).toMatch(/fromAPIKey/);
    });
  });
  
  describe('File Upload Functionality', () => {
    test('prepares media object with mime type', () => {
      expect(sampleCode).toMatch(/mimeType:\s*mime\.lookup/);
    });
    
    test('creates read stream from file', () => {
      expect(sampleCode).toMatch(/fs\.createReadStream\(filePath\)/);
    });
    
    test('includes display name in request body', () => {
      expect(sampleCode).toMatch(/displayName/);
      expect(sampleCode).toMatch(/fileDisplayName/);
    });
    
    test('calls genaiService.media.upload', () => {
      expect(sampleCode).toMatch(/genaiService\.media\.upload/);
    });
    
    test('extracts file URI from response', () => {
      expect(sampleCode).toMatch(/file\.uri/);
      expect(sampleCode).toMatch(/fileUri/);
    });
  });
  
  describe('Content Generation', () => {
    test('defines generation prompt', () => {
      expect(sampleCode).toMatch(/prompt/);
      expect(sampleCode).toMatch(/Describe the image/);
    });
    
    test('uses gemini-2.5-flash model', () => {
      expect(sampleCode).toMatch(/gemini-2\.5-flash/);
    });
    
    test('constructs contents with text and file_data', () => {
      expect(sampleCode).toMatch(/contents/);
      expect(sampleCode).toMatch(/parts/);
      expect(sampleCode).toMatch(/text/);
      expect(sampleCode).toMatch(/file_data/);
    });
    
    test('includes file_uri in file_data', () => {
      expect(sampleCode).toMatch(/file_uri/);
    });
    
    test('includes mime_type in file_data', () => {
      expect(sampleCode).toMatch(/mime_type/);
    });
    
    test('calls generateContent method', () => {
      expect(sampleCode).toMatch(/generateContent/);
    });
    
    test('prints response data', () => {
      expect(sampleCode).toMatch(/console\.log/);
      expect(sampleCode).toMatch(/generateContentResponse\.data/);
    });
  });
  
  describe('Error Handling', () => {
    test('has try-catch block', () => {
      expect(sampleCode).toMatch(/try\s*\{/);
      expect(sampleCode).toMatch(/catch\s*\(/);
    });
    
    test('throws caught errors', () => {
      expect(sampleCode).toMatch(/throw err/);
    });
  });
  
  describe('Async Function', () => {
    test('defines async run function', () => {
      expect(sampleCode).toMatch(/async\s+function\s+run/);
    });
    
    test('run function accepts filePath parameter', () => {
      expect(sampleCode).toMatch(/function\s+run\s*\(\s*filePath/);
    });
    
    test('run function accepts fileDisplayName parameter', () => {
      expect(sampleCode).toMatch(/fileDisplayName/);
    });
  });
  
  describe('Sample Execution', () => {
    test('defines sample file path', () => {
      expect(sampleCode).toMatch(/filePath\s*=/);
      expect(sampleCode).toMatch(/sample_data\/gemini_logo\.png/);
    });
    
    test('defines file display name', () => {
      expect(sampleCode).toMatch(/fileDisplayName\s*=/);
      expect(sampleCode).toMatch(/Gemini logo/);
    });
    
    test('calls run function with parameters', () => {
      expect(sampleCode).toMatch(/run\s*\(\s*filePath\s*,\s*fileDisplayName\s*\)/);
    });
  });
  
  describe('Code Quality', () => {
    test('uses const for immutable variables', () => {
      const constMatches = sampleCode.match(/const\s+/g);
      expect(constMatches).not.toBeNull();
      expect(constMatches.length).toBeGreaterThan(5);
    });
    
    test('uses await for async operations', () => {
      expect(sampleCode).toMatch(/await/);
    });
    
    test('has comments explaining key sections', () => {
      const comments = sampleCode.match(/\/\//g);
      expect(comments).not.toBeNull();
      expect(comments.length).toBeGreaterThan(3);
    });
  });
  
  describe('API Endpoints', () => {
    test('uses correct discovery API URL', () => {
      expect(sampleCode).toMatch(/\$discovery\/rest/);
    });
    
    test('includes API key in discovery URL', () => {
      expect(sampleCode).toMatch(/key=\$\{API_KEY\}/);
    });
  });
});

describe('File API Integration Tests', () => {
  describe('Model Configuration', () => {
    test('model path follows correct format', () => {
      const modelPattern = /models\/gemini-[\d.]+-[a-z]+/;
      expect(sampleCode).toMatch(modelPattern);
    });
  });
  
  describe('Request Structure', () => {
    test('request body includes model parameter', () => {
      expect(sampleCode).toMatch(/model:\s*model/);
    });
    
    test('request body includes contents', () => {
      expect(sampleCode).toMatch(/requestBody:\s*contents/);
    });
    
    test('request includes auth parameter', () => {
      expect(sampleCode).toMatch(/auth:\s*auth/);
    });
  });
});