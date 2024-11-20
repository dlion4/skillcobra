import React from "react";
import { Sitemap } from "./pages/Sitemap";

export const App = ({ id }: { id: string }) => {
  return (
    <>
      <Sitemap id={id} />
    </>
  );
};
