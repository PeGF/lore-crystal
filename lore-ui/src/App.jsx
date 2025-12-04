import { BrowserRouter, Routes, Route } from "react-router-dom";
import ArcaneChat from "./pages/ArcaneChat";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ArcaneChat />} />
      </Routes>
    </BrowserRouter>
  );
}
