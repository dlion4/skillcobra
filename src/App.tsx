import React from "react";
import CourseForm from "./pages/CreateCourse";

export const App = ({ id }: { id: string }) => {
  if (id == "app") {
    return <CourseForm />;
  }
  return <></>;
};
