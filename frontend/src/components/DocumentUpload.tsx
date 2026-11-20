
import { useRef, useState } from "react";
import { Upload, CheckCircle, AlertCircle } from "lucide-react";
import api from "../services/api";

interface DocumentUploadProps {
  onUploadSuccess?: () => void;
}

interface UploadResult {
  message: string;
  original_filename: string;
  result: {
    total_chunks: number;
    stored_vectors: number;
    status: string;
  };
}

export default function DocumentUpload({
  onUploadSuccess,
}: DocumentUploadProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState(false);

  const handleUpload = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const allowed = [".pdf", ".docx", ".txt"];
    const extension = file.name
      .slice(file.name.lastIndexOf("."))
      .toLowerCase();

    if (!allowed.includes(extension)) {
      setError(true);
      setMessage("Only PDF, DOCX and TXT files are supported.");
      event.target.value = "";
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setError(false);
    setMessage("");

    try {
      const response = await api.post<UploadResult>(
  "/documents/upload",
  formData
);

console.log("UPLOAD RESPONSE:", response.data);

setMessage(
  `${response.data.original_filename} uploaded successfully. ${response.data.result.stored_vectors} chunks indexed.`
);

setError(false);
onUploadSuccess?.();
    } catch (err: any) {
      setError(true);
      setMessage(
        err.response?.data?.detail || "Document upload failed."
      );
    } finally {
      setLoading(false);
      event.target.value = "";
    }
  };

  return (
    <div className="rounded-2xl border border-dashed border-slate-700 bg-slate-950 p-10 text-center">
      <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-2xl bg-blue-500/10">
        <Upload className="text-blue-400" size={30} />
      </div>

      <h3 className="text-xl font-semibold text-white">
        Upload your documents
      </h3>

      <p className="mx-auto mt-2 max-w-lg text-sm text-slate-400">
        Upload PDF, DOCX or TXT files to create your searchable AI knowledge base.
      </p>

      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.docx,.txt"
        className="hidden"
        onChange={handleUpload}
      />

      <button
        onClick={() => inputRef.current?.click()}
        disabled={loading}
        className="mt-6 rounded-lg bg-blue-600 px-6 py-3 text-sm font-semibold text-white hover:bg-blue-700 disabled:opacity-50"
      >
        <Upload className="mr-2 inline" size={17} />
        {loading ? "Processing..." : "Upload Document"}
      </button>

      {message && (
        <div className={`mx-auto mt-5 flex max-w-xl items-center justify-center gap-2 text-sm ${
          error ? "text-red-400" : "text-green-400"
        }`}>
          {error ? <AlertCircle size={18} /> : <CheckCircle size={18} />}
          {message}
        </div>
      )}
    </div>
  );
}
