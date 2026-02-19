const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

export const fetchAnalysis = async (file, drugName) => {
  const formData = new FormData();
  formData.append("file", file);

  // The 'drug' parameter must be appended to the URL for @router.post to see it as a Query parameter
  const url = `${API_BASE_URL}/analyze?drug=${encodeURIComponent(drugName)}`;

  const response = await fetch(url, {
    method: "POST",
    body: formData,
  });
  
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "Analysis failed");
  }
  
  return await response.json();
};