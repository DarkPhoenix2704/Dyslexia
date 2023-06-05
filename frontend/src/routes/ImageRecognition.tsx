import { useState } from "react";

export const ImageRecognition = () => {
  const [file, setFile] = useState<File | null>(null);
  const [isDyslexic, setIsDyslexic] = useState<boolean | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  return (
    <div className="flex flex-col h-[100vh] items-center justify-center gap-3 bg-[#141414] text-white">
      <h1 className="text-5xl text-center">
        Dyslexia Diagnosis using Machine Learning (HandWriting)
      </h1>
      {file && (
        <img
          src={URL.createObjectURL(file)}
          alt="fruit"
          className="mt-4 w-3/4 md:w-96 rounded-md"
        />
      )}
      <input
        type="file"
        className="mt-4 "
        onChange={(e) => {
          if (e.target.files) {
            setFile(e.target.files[0]);
          }
        }}
      />
      <button
        className=" bg-[#1f1f1f] text-xl gap-2 px-2 flex flex-row items-center justify-center py-2 rounded-md text-[#ffffff] hover:bg-[#141414]"
        onClick={() => {
          if (file) {
            setIsDyslexic(null);
            setIsLoading(true);
            const formData = new FormData();
            formData.append("file", file);
            fetch("http://localhost:5000/image", {
              method: "POST",
              body: formData,
            })
              .then((res) => res.json())
              .then((data) => {
                setIsDyslexic(data.isDyslexic);
              })
              .finally(() => {
                setIsLoading(false);
              });
          }
        }}
      >
        {isLoading ? (
          <svg
            className="animate-spin h-5 w-5 text-white"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
            ></circle>
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
        ) : (
          <></>
        )}
        Detect Dyslexia
      </button>
      {isDyslexic !== null && (
        <h1 className="text-2xl text-center">
          {isDyslexic ? "You May be Dyslexic" : "Not Dyslexic"}
        </h1>
      )}
    </div>
  );
};
