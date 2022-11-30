// Understanding async/await
import UIKit


enum ErrorResponse: Error {
    case invalidUrl
    case invalidResponse
    case invalidData
}

struct Quote: Codable {
    var text: String?
    var author: String?
}

class ApiServiceQuote {
    // SSE 資料會以 data: {} 方式傳遞，先簡單濾掉 data: 字串
    func decodeStreamData(_ line: String) -> String? {
        let contents = line.components(separatedBy: "data:")
        guard contents.count >= 1 else {
            return nil
        }
        return contents[1]
    }
    
    func streamOneSameQuotes() async throws {
        guard let url = URL(string: "http://127.0.0.1:8000/oneSameQuote") else {
//        guard let url = URL(string: "http://127.0.0.1:8000/stream/oneSameQuote") else {
            throw ErrorResponse.invalidUrl
        }

        let (bytes, response) = try await URLSession.shared.bytes(from: url)
        
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw ErrorResponse.invalidResponse
        }
        
        for try await line in bytes.lines {
//            print("Line: \(line)")
//            guard let line = decodeStreamData(line) else {
//                throw ErrorResponse.invalidData
//            }
            
            let quote = try JSONDecoder().decode(Quote.self, from: Data(line.utf8))
//            print(quote)
            guard let text = quote.text, let author = quote.author else {
                throw ErrorResponse.invalidData
            }

            print("\(author) says: \"\(text)\" ")
        }
    }
    
    func streamOneDifferentQuotes() async throws {
        guard let url = URL(string: "http://127.0.0.1:8000/oneDifferentQuote") else {
        //guard let url = URL(string: "http://127.0.0.1:8000/stream/oneDifferentQuote") else {
            throw ErrorResponse.invalidUrl
        }
        
        let (bytes, response) = try await URLSession.shared.bytes(from: url)
        
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw ErrorResponse.invalidResponse
        }
        
        for try await line in bytes.lines {
            //print("Line: \(line)")
//            guard let line = decodeStreamData(line) else {
//                throw ErrorResponse.invalidData
//            }

            let quote = try JSONDecoder().decode(Quote.self, from: Data(line.utf8))
                //            print(quote)
            guard let text = quote.text, let author = quote.author else {
                throw ErrorResponse.invalidData
            }
            
            print("\(author) says: \"\(text)\" ")
        }
    }

    func streamManySameQuotes() async throws {
        guard let url = URL(string: "http://127.0.0.1:8000/manySameQuote") else {
        //guard let url = URL(string: "http://127.0.0.1:8000/stream/manySameQuote") else {
            throw ErrorResponse.invalidUrl
        }
        
        let (bytes, response) = try await URLSession.shared.bytes(from: url)
        
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw ErrorResponse.invalidResponse
        }
        
        for try await line in bytes.lines {
//                            print("Line: \(line)")
//                            guard let line = decodeStreamData(line) else {
//                                throw ErrorResponse.invalidData
//                            }
            
            let quote = try JSONDecoder().decode([Quote].self, from: Data(line.utf8))
//                            print(quote)
            
            for q in quote {
                guard let text = q.text, let author = q.author else {
                    throw ErrorResponse.invalidData
                }
                
                print("\(author) says: \"\(text)\" ")
            }
        }
    }

    func streamManyDifferentQuotes() async throws {
        //guard let url = URL(string: "http://127.0.0.1:8000/manyDifferentQuote") else {
        guard let url = URL(string: "http://127.0.0.1:8000/stream/manyDifferentQuote") else {
            throw ErrorResponse.invalidUrl
        }
        
        let (bytes, response) = try await URLSession.shared.bytes(from: url)
        
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw ErrorResponse.invalidResponse
        }
        
        for try await line in bytes.lines {
                //                            print("Line: \(line)")
                                            guard let line = decodeStreamData(line) else {
                                                throw ErrorResponse.invalidData
                                            }
            
            let quote = try JSONDecoder().decode([Quote].self, from: Data(line.utf8))
                //                            print(quote)
            
            for q in quote {
                guard let text = q.text, let author = q.author else {
                    throw ErrorResponse.invalidData
                }
                
                print("\(author) says: \"\(text)\" ")
            }
        }
    }

}

// Wrap our call in "Task" to allow this asynchronous function
// to be called from Playgrounds 'Synchronous' flow
Task {
    try await ApiServiceQuote().streamOneSameQuotes()
    //try await ApiServiceQuote().streamOneDifferentQuotes()
    //try await ApiServiceQuote().streamManySameQuotes()
    //try await ApiServiceQuote().streamManyDifferentQuotes()
}

