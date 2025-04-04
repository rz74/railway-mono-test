import React from "react";
import ImageUploadGrid from "./components/ImageUploadGrid";

const App = () => {
  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <main className="space-y-6">
        <ImageUploadGrid />
      </main>
    </div>
  );
};

export default App;
