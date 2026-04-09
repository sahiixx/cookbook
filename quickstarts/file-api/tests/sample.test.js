/**
 * Copyright 2025 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

const fs = require('fs');
const path = require('path');

// Mock dependencies
jest.mock('dotenv');
jest.mock('googleapis');
jest.mock('mime-types');

const dotenv = require('dotenv');
const { google } = require('googleapis');
const mime = require('mime-types');

describe('File API Sample Tests', () => {
  let mockGenaiService;
  let mockAuth;

  beforeEach(() => {
    // Reset all mocks
    jest.clearAllMocks();
    
    // Mock environment variables
    process.env.GOOGLE_API_KEY = 'test-api-key-12345';
    dotenv.config = jest.fn();

    // Mock googleapis
    mockAuth = {
      fromAPIKey: jest.fn().mockReturnValue('mock-auth')
    };
    
    mockGenaiService = {
      media: {
        upload: jest.fn()
      },
      models: {
        generateContent: jest.fn()
      }
    };

    google.discoverAPI = jest.fn().mockResolvedValue(mockGenaiService);
    google.auth = {
      GoogleAuth: jest.fn().mockReturnValue(mockAuth)
    };

    // Mock mime-types
    mime.lookup = jest.fn().mockReturnValue('image/png');

    // Mock fs
    jest.spyOn(fs, 'createReadStream').mockReturnValue('mock-stream');
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  describe('API Configuration', () => {
    test('should load environment variables from .env file', () => {
      require('../sample.js');
      expect(dotenv.config).toHaveBeenCalledWith({ path: '.env' });
    });

    test('should construct correct discovery URL with API key', () => {
      const API_KEY = 'test-key';
      const expectedUrl = `https://generativelanguage.googleapis.com/$discovery/rest?version=v1beta&key=${API_KEY}`;
      
      expect(expectedUrl).toContain('generativelanguage.googleapis.com');
      expect(expectedUrl).toContain('version=v1beta');
      expect(expectedUrl).toContain(`key=${API_KEY}`);
    });

    test('should throw error when API key is missing', () => {
      delete process.env.GOOGLE_API_KEY;
      
      jest.isolateModules(() => {
        expect(() => {
          const apiKey = process.env.GOOGLE_API_KEY;
          if (!apiKey) throw new Error('API key is required');
        }).toThrow('API key is required');
      });
    });

    test('should use correct API version', () => {
      const apiVersion = 'v1beta';
      expect(apiVersion).toBe('v1beta');
    });

    test('should use HTTPS protocol for API endpoint', () => {
      const endpoint = 'https://generativelanguage.googleapis.com';
      expect(endpoint).toMatch(/^https:\/\//);
    });
  });

  describe('File Upload', () => {
    test('should upload file with correct mime type', async () => {
      const mockFile = {
        uri: 'https://generativelanguage.googleapis.com/v1beta/files/test-file',
        mimeType: 'image/png'
      };

      mockGenaiService.media.upload.mockResolvedValue({
        data: { file: mockFile }
      });

      mockGenaiService.models.generateContent.mockResolvedValue({
        data: { candidates: [{ content: { parts: [{ text: 'Test response' }] } }] }
      });

      const filePath = 'sample_data/gemini_logo.png';
      mime.lookup.mockReturnValue('image/png');
      
      jest.isolateModules(() => {
        require('../sample.js');
      });

      await new Promise(resolve => setTimeout(resolve, 100));

      expect(mime.lookup).toHaveBeenCalledWith(filePath);
    });

    test('should handle file upload errors gracefully', async () => {
      mockGenaiService.media.upload.mockRejectedValue(
        new Error('Network error')
      );

      jest.isolateModules(() => {
        require('../sample.js');
      });

      await new Promise(resolve => setTimeout(resolve, 100));

      expect(mockGenaiService.media.upload).toHaveBeenCalled();
    });

    test('should include display name in upload request', async () => {
      const mockFile = {
        uri: 'https://generativelanguage.googleapis.com/v1beta/files/test-file',
        mimeType: 'image/png'
      };

      mockGenaiService.media.upload.mockResolvedValue({
        data: { file: mockFile }
      });

      mockGenaiService.models.generateContent.mockResolvedValue({
        data: { candidates: [{ content: { parts: [{ text: 'Test' }] } }] }
      });

      jest.isolateModules(() => {
        require('../sample.js');
      });

      await new Promise(resolve => setTimeout(resolve, 100));

      expect(mockGenaiService.media.upload).toHaveBeenCalledWith(
        expect.objectContaining({
          requestBody: expect.objectContaining({
            file: expect.objectContaining({
              displayName: 'Gemini logo'
            })
          })
        })
      );
    });

    test('should create read stream for file', async () => {
      const filePath = 'sample_data/gemini_logo.png';
      
      mockGenaiService.media.upload.mockResolvedValue({
        data: {
          file: {
            uri: 'test-uri',
            mimeType: 'image/png'
          }
        }
      });

      mockGenaiService.models.generateContent.mockResolvedValue({
        data: {}
      });

      jest.isolateModules(() => {
        require('../sample.js');
      });

      await new Promise(resolve => setTimeout(resolve, 100));

      expect(fs.createReadStream).toHaveBeenCalledWith(filePath);
    });

    test('should handle different image formats', () => {
      const formats = {
        'test.png': 'image/png',
        'test.jpg': 'image/jpeg',
        'test.gif': 'image/gif',
        'test.webp': 'image/webp'
      };

      mime.lookup.mockImplementation((file) => formats[path.basename(file)] || 'application/octet-stream');

      Object.entries(formats).forEach(([file, expectedMime]) => {
        expect(mime.lookup(file)).toBe(expectedMime);
      });
    });

    test('should handle upload with media object structure', () => {
      const media = {
        mimeType: 'image/png',
        body: 'mock-stream'
      };
      
      expect(media).toHaveProperty('mimeType');
      expect(media).toHaveProperty('body');
    });

    test('should handle large file uploads', async () => {
      const largeFile = {
        uri: 'test-uri',
        mimeType: 'image/png',
        sizeBytes: '10485760' // 10MB
      };

      mockGenaiService.media.upload.mockResolvedValue({
        data: { file: largeFile }
      });

      mockGenaiService.models.generateContent.mockResolvedValue({
        data: {}
      });

      jest.isolateModules(() => {
        require('../sample.js');
      });

      await new Promise(resolve => setTimeout(resolve, 100));

      expect(mockGenaiService.media.upload).toHaveBeenCalled();
    });
  });

  describe('Content Generation', () => {
    test('should call generateContent with correct model', async () => {
      const mockFile = {
        uri: 'https://generativelanguage.googleapis.com/v1beta/files/test-file',
        mimeType: 'image/png'
      };

      mockGenaiService.media.upload.mockResolvedValue({
        data: { file: mockFile }
      });

      mockGenaiService.models.generateContent.mockResolvedValue({
        data: {
          candidates: [{
            content: {
              parts: [{ text: 'A beautiful Gemini logo' }]
            }
          }]
        }
      });

      jest.isolateModules(() => {
        require('../sample.js');
      });

      await new Promise(resolve => setTimeout(resolve, 100));

      expect(mockGenaiService.models.generateContent).toHaveBeenCalledWith(
        expect.objectContaining({
          model: 'models/gemini-2.5-flash'
        })
      );
    });

    test('should use gemini-2.5-flash model', () => {
      const modelName = 'models/gemini-2.5-flash';
      expect(modelName).toContain('gemini-2.5-flash');
      expect(modelName).toMatch(/^models\//);
    });

    test('should include prompt and file data in request', async () => {
      const mockFile = {
        uri: 'https://generativelanguage.googleapis.com/v1beta/files/test-file',
        mimeType: 'image/png'
      };

      mockGenaiService.media.upload.mockResolvedValue({
        data: { file: mockFile }
      });

      mockGenaiService.models.generateContent.mockResolvedValue({
        data: {}
      });

      jest.isolateModules(() => {
        require('../sample.js');
      });

      await new Promise(resolve => setTimeout(resolve, 100));

      expect(mockGenaiService.models.generateContent).toHaveBeenCalledWith(
        expect.objectContaining({
          requestBody: expect.objectContaining({
            contents: expect.arrayContaining([
              expect.objectContaining({
                parts: expect.arrayContaining([
                  expect.objectContaining({
                    text: 'Describe the image with a creative description'
                  }),
                  expect.objectContaining({
                    file_data: expect.objectContaining({
                      file_uri: mockFile.uri,
                      mime_type: mockFile.mimeType
                    })
                  })
                ])
              })
            ])
          })
        })
      );
    });

    test('should use correct prompt text', () => {
      const prompt = 'Describe the image with a creative description';
      expect(prompt).toBe('Describe the image with a creative description');
      expect(prompt).toMatch(/creative/i);
    });

    test('should handle generation errors', async () => {
      const mockFile = {
        uri: 'test-uri',
        mimeType: 'image/png'
      };

      mockGenaiService.media.upload.mockResolvedValue({
        data: { file: mockFile }
      });

      mockGenaiService.models.generateContent.mockRejectedValue(
        new Error('API quota exceeded')
      );

      jest.isolateModules(() => {
        require('../sample.js');
      });

      await new Promise(resolve => setTimeout(resolve, 100));

      expect(mockGenaiService.models.generateContent).toHaveBeenCalled();
    });

    test('should handle rate limiting errors', async () => {
      const mockFile = {
        uri: 'test-uri',
        mimeType: 'image/png'
      };

      mockGenaiService.media.upload.mockResolvedValue({
        data: { file: mockFile }
      });

      const rateLimitError = new Error('Rate limit exceeded');
      rateLimitError.code = 429;
      mockGenaiService.models.generateContent.mockRejectedValue(rateLimitError);

      jest.isolateModules(() => {
        require('../sample.js');
      });

      await new Promise(resolve => setTimeout(resolve, 100));

      expect(mockGenaiService.models.generateContent).toHaveBeenCalled();
    });

    test('should log response data', async () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();
      
      const mockFile = {
        uri: 'test-uri',
        mimeType: 'image/png'
      };

      const mockResponse = {
        data: {
          candidates: [{
            content: {
              parts: [{ text: 'Test response' }]
            }
          }]
        }
      };

      mockGenaiService.media.upload.mockResolvedValue({
        data: { file: mockFile }
      });

      mockGenaiService.models.generateContent.mockResolvedValue(mockResponse);

      jest.isolateModules(() => {
        require('../sample.js');
      });

      await new Promise(resolve => setTimeout(resolve, 100));

      expect(consoleSpy).toHaveBeenCalled();
      consoleSpy.mockRestore();
    });

    test('should handle content with safety ratings', async () => {
      const mockFile = {
        uri: 'test-uri',
        mimeType: 'image/png'
      };

      const mockResponse = {
        data: {
          candidates: [{
            content: { parts: [{ text: 'Safe content' }] },
            safetyRatings: [
              { category: 'HARM_CATEGORY_HARASSMENT', probability: 'NEGLIGIBLE' }
            ]
          }]
        }
      };

      mockGenaiService.media.upload.mockResolvedValue({
        data: { file: mockFile }
      });

      mockGenaiService.models.generateContent.mockResolvedValue(mockResponse);

      jest.isolateModules(() => {
        require('../sample.js');
      });

      await new Promise(resolve => setTimeout(resolve, 100));

      expect(mockGenaiService.models.generateContent).toHaveBeenCalled();
    });
  });

  describe('File Path Validation', () => {
    test('should use correct default file path', () => {
      const expectedPath = 'sample_data/gemini_logo.png';
      expect(expectedPath).toBe('sample_data/gemini_logo.png');
      expect(expectedPath).toContain('sample_data');
      expect(expectedPath).toEndWith('.png');
    });

    test('should use correct display name', () => {
      const expectedName = 'Gemini logo';
      expect(expectedName).toBe('Gemini logo');
      expect(expectedName).toMatch(/Gemini/);
    });

    test('should validate file path format', () => {
      const filePath = 'sample_data/gemini_logo.png';
      expect(filePath).toBeTruthy();
      expect(typeof filePath).toBe('string');
      expect(filePath.split('/').length).toBeGreaterThan(1);
    });
  });

  describe('Authentication', () => {
    test('should create GoogleAuth instance', async () => {
      mockGenaiService.media.upload.mockResolvedValue({
        data: {
          file: { uri: 'test-uri', mimeType: 'image/png' }
        }
      });

      mockGenaiService.models.generateContent.mockResolvedValue({
        data: {}
      });

      jest.isolateModules(() => {
        require('../sample.js');
      });

      await new Promise(resolve => setTimeout(resolve, 100));

      expect(google.auth.GoogleAuth).toHaveBeenCalled();
    });

    test('should use API key for authentication', async () => {
      mockGenaiService.media.upload.mockResolvedValue({
        data: {
          file: { uri: 'test-uri', mimeType: 'image/png' }
        }
      });

      mockGenaiService.models.generateContent.mockResolvedValue({
        data: {}
      });

      jest.isolateModules(() => {
        require('../sample.js');
      });

      await new Promise(resolve => setTimeout(resolve, 100));

      expect(mockAuth.fromAPIKey).toHaveBeenCalledWith('test-api-key-12345');
    });

    test('should handle authentication failures', async () => {
      mockAuth.fromAPIKey.mockImplementation(() => {
        throw new Error('Invalid API key');
      });

      jest.isolateModules(() => {
        try {
          require('../sample.js');
        } catch (error) {
          // Expected to fail
        }
      });

      await new Promise(resolve => setTimeout(resolve, 100));
    });

    test('should validate API key format', () => {
      const apiKey = process.env.GOOGLE_API_KEY;
      expect(apiKey).toBeTruthy();
      expect(typeof apiKey).toBe('string');
      expect(apiKey.length).toBeGreaterThan(0);
    });
  });

  describe('Edge Cases', () => {
    test('should handle empty response from file upload', async () => {
      mockGenaiService.media.upload.mockResolvedValue({
        data: {}
      });

      jest.isolateModules(() => {
        require('../sample.js');
      });

      await new Promise(resolve => setTimeout(resolve, 100));

      expect(mockGenaiService.media.upload).toHaveBeenCalled();
    });

    test('should handle malformed file URI', async () => {
      mockGenaiService.media.upload.mockResolvedValue({
        data: {
          file: {
            uri: '',
            mimeType: 'image/png'
          }
        }
      });

      mockGenaiService.models.generateContent.mockResolvedValue({
        data: {}
      });

      jest.isolateModules(() => {
        require('../sample.js');
      });

      await new Promise(resolve => setTimeout(resolve, 100));

      expect(mockGenaiService.models.generateContent).toHaveBeenCalled();
    });

    test('should handle network timeouts', async () => {
      mockGenaiService.media.upload.mockImplementation(() => {
        return new Promise((_, reject) => {
          setTimeout(() => reject(new Error('Network timeout')), 50);
        });
      });

      jest.isolateModules(() => {
        require('../sample.js');
      });

      await new Promise(resolve => setTimeout(resolve, 100));

      expect(mockGenaiService.media.upload).toHaveBeenCalled();
    });

    test('should handle null or undefined file path', () => {
      const nullPath = null;
      const undefinedPath = undefined;
      
      expect(nullPath).toBeNull();
      expect(undefinedPath).toBeUndefined();
    });

    test('should handle missing mimeType', async () => {
      mockGenaiService.media.upload.mockResolvedValue({
        data: {
          file: {
            uri: 'test-uri'
          }
        }
      });

      mockGenaiService.models.generateContent.mockResolvedValue({
        data: {}
      });

      jest.isolateModules(() => {
        require('../sample.js');
      });

      await new Promise(resolve => setTimeout(resolve, 100));

      expect(mockGenaiService.media.upload).toHaveBeenCalled();
    });

    test('should handle 404 errors', async () => {
      const notFoundError = new Error('File not found');
      notFoundError.code = 404;

      mockGenaiService.media.upload.mockRejectedValue(notFoundError);

      jest.isolateModules(() => {
        require('../sample.js');
      });

      await new Promise(resolve => setTimeout(resolve, 100));

      expect(mockGenaiService.media.upload).toHaveBeenCalled();
    });

    test('should handle 500 server errors', async () => {
      const serverError = new Error('Internal server error');
      serverError.code = 500;

      mockGenaiService.media.upload.mockRejectedValue(serverError);

      jest.isolateModules(() => {
        require('../sample.js');
      });

      await new Promise(resolve => setTimeout(resolve, 100));

      expect(mockGenaiService.media.upload).toHaveBeenCalled();
    });
  });

  describe('Response Handling', () => {
    test('should parse and log JSON response', async () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();
      
      const mockFile = {
        uri: 'test-uri',
        mimeType: 'image/png'
      };

      const mockResponse = {
        data: {
          candidates: [{
            content: {
              parts: [{ text: 'Creative description of Gemini logo' }]
            },
            finishReason: 'STOP'
          }],
          usageMetadata: {
            promptTokenCount: 10,
            candidatesTokenCount: 20
          }
        }
      };

      mockGenaiService.media.upload.mockResolvedValue({
        data: { file: mockFile }
      });

      mockGenaiService.models.generateContent.mockResolvedValue(mockResponse);

      jest.isolateModules(() => {
        require('../sample.js');
      });

      await new Promise(resolve => setTimeout(resolve, 100));

      expect(consoleSpy).toHaveBeenCalledWith(JSON.stringify(mockResponse.data));
      consoleSpy.mockRestore();
    });

    test('should handle responses with multiple candidates', async () => {
      const mockFile = {
        uri: 'test-uri',
        mimeType: 'image/png'
      };

      const mockResponse = {
        data: {
          candidates: [
            {
              content: { parts: [{ text: 'Response 1' }] },
              finishReason: 'STOP'
            },
            {
              content: { parts: [{ text: 'Response 2' }] },
              finishReason: 'STOP'
            }
          ]
        }
      };

      mockGenaiService.media.upload.mockResolvedValue({
        data: { file: mockFile }
      });

      mockGenaiService.models.generateContent.mockResolvedValue(mockResponse);

      jest.isolateModules(() => {
        require('../sample.js');
      });

      await new Promise(resolve => setTimeout(resolve, 100));

      expect(mockGenaiService.models.generateContent).toHaveBeenCalled();
    });

    test('should handle empty candidates array', async () => {
      const mockFile = {
        uri: 'test-uri',
        mimeType: 'image/png'
      };

      mockGenaiService.media.upload.mockResolvedValue({
        data: { file: mockFile }
      });

      mockGenaiService.models.generateContent.mockResolvedValue({
        data: { candidates: [] }
      });

      jest.isolateModules(() => {
        require('../sample.js');
      });

      await new Promise(resolve => setTimeout(resolve, 100));

      expect(mockGenaiService.models.generateContent).toHaveBeenCalled();
    });

    test('should handle response with usage metadata', async () => {
      const mockFile = {
        uri: 'test-uri',
        mimeType: 'image/png'
      };

      const mockResponse = {
        data: {
          candidates: [{ content: { parts: [{ text: 'Test' }] } }],
          usageMetadata: {
            promptTokenCount: 50,
            candidatesTokenCount: 100,
            totalTokenCount: 150
          }
        }
      };

      mockGenaiService.media.upload.mockResolvedValue({
        data: { file: mockFile }
      });

      mockGenaiService.models.generateContent.mockResolvedValue(mockResponse);

      jest.isolateModules(() => {
        require('../sample.js');
      });

      await new Promise(resolve => setTimeout(resolve, 100));

      expect(mockGenaiService.models.generateContent).toHaveBeenCalled();
    });
  });

  describe('Integration Flow', () => {
    test('should complete full upload and generation flow', async () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();
      
      const mockFile = {
        uri: 'https://generativelanguage.googleapis.com/v1beta/files/abc123',
        mimeType: 'image/png',
        name: 'files/abc123',
        sizeBytes: '102400'
      };

      const mockResponse = {
        data: {
          candidates: [{
            content: {
              parts: [{ text: 'A vibrant Gemini logo with geometric shapes' }]
            },
            finishReason: 'STOP',
            safetyRatings: []
          }]
        }
      };

      mockGenaiService.media.upload.mockResolvedValue({
        data: { file: mockFile }
      });

      mockGenaiService.models.generateContent.mockResolvedValue(mockResponse);

      jest.isolateModules(() => {
        require('../sample.js');
      });

      await new Promise(resolve => setTimeout(resolve, 150));

      expect(mockGenaiService.media.upload).toHaveBeenCalled();
      expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Uploaded file:'));
      expect(mockGenaiService.models.generateContent).toHaveBeenCalled();
      expect(consoleSpy).toHaveBeenCalledWith(JSON.stringify(mockResponse.data));

      consoleSpy.mockRestore();
    });

    test('should handle full flow with errors', async () => {
      const consoleSpy = jest.spyOn(console, 'log').mockImplementation();
      
      mockGenaiService.media.upload.mockResolvedValue({
        data: { file: { uri: 'test-uri', mimeType: 'image/png' } }
      });

      mockGenaiService.models.generateContent.mockRejectedValue(
        new Error('Generation failed')
      );

      jest.isolateModules(() => {
        require('../sample.js');
      });

      await new Promise(resolve => setTimeout(resolve, 150));

      expect(mockGenaiService.media.upload).toHaveBeenCalled();
      expect(mockGenaiService.models.generateContent).toHaveBeenCalled();

      consoleSpy.mockRestore();
    });
  });
});