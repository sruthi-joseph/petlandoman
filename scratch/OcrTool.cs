using System;
using System.IO;
using System.Threading.Tasks;
using Windows.Storage;
using Windows.Graphics.Imaging;
using Windows.Media.Ocr;

class Program {
    static void Main(string[] args) {
        if (args.Length == 0) {
            Console.WriteLine("Usage: OcrTool.exe <directory_path>");
            return;
        }

        string dirPath = args[0];
        if (!Directory.Exists(dirPath)) {
            Console.WriteLine("Directory does not exist: " + dirPath);
            return;
        }

        Console.WriteLine("Scanning directory: " + dirPath);
        Console.WriteLine("========================================");
        
        var files = Directory.GetFiles(dirPath);
        foreach (var file in files) {
            string ext = Path.GetExtension(file).ToLower();
            if (ext == ".png" || ext == ".jpg" || ext == ".jpeg" || ext == ".bmp") {
                try {
                    string text = ProcessImage(file);
                    Console.WriteLine("FILE: " + Path.GetFileName(file));
                    if (string.IsNullOrWhiteSpace(text)) {
                        Console.WriteLine("TEXT: [No text found]");
                    } else {
                        Console.WriteLine("TEXT: " + text.Replace("\r", " ").Replace("\n", " "));
                    }
                    Console.WriteLine("--------------------------------------");
                } catch (Exception ex) {
                    Console.WriteLine("FILE: " + Path.GetFileName(file) + " - ERROR: " + ex.Message + " | " + ex.InnerException?.Message);
                    Console.WriteLine("--------------------------------------");
                }
            }
        }
    }

    static string ProcessImage(string path) {
        string absPath = Path.GetFullPath(path);
        
        // Get File
        var fileOp = StorageFile.GetFileFromPathAsync(absPath);
        var fileTask = WindowsRuntimeSystemExtensions.AsTask(fileOp);
        fileTask.Wait();
        var file = fileTask.Result;
        
        // Open Stream
        var streamOp = file.OpenAsync(FileAccessMode.Read);
        var streamTask = WindowsRuntimeSystemExtensions.AsTask(streamOp);
        streamTask.Wait();
        
        using (var stream = streamTask.Result) {
            // Get Decoder
            var decoderOp = BitmapDecoder.CreateAsync(stream);
            var decoderTask = WindowsRuntimeSystemExtensions.AsTask(decoderOp);
            decoderTask.Wait();
            var decoder = decoderTask.Result;
            
            // Get SoftwareBitmap
            var bitmapOp = decoder.GetSoftwareBitmapAsync();
            var bitmapTask = WindowsRuntimeSystemExtensions.AsTask(bitmapOp);
            bitmapTask.Wait();
            
            using (var softwareBitmap = bitmapTask.Result) {
                var ocrEngine = OcrEngine.TryCreateFromUserProfileLanguages();
                if (ocrEngine == null) {
                    return "[OCR Engine not available]";
                }
                
                // Recognize OCR
                var ocrOp = ocrEngine.RecognizeAsync(softwareBitmap);
                var ocrTask = WindowsRuntimeSystemExtensions.AsTask(ocrOp);
                ocrTask.Wait();
                return ocrTask.Result.Text;
            }
        }
    }
}
