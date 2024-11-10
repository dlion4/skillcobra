import React, { useState, useEffect } from "react";

// Define the Category type for TypeScript
type Category = {
  id: number;
  name: string;
};

const CourseForm: React.FC = () => {
  // Local state to store form data
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    courseDescription: "",
    whatStudentsLearn: "",
    requirements: "",
    courseLevel: "",
    audioLanguage: [],
    closeCaption: [],
    category: "",
  });

  const [categories, setCategories] = useState<Category[]>([]);

  // Fetch categories from Django backend (example API endpoint)
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await fetch("/api/courses/categories"); // Adjust the API endpoint as needed
        const data = await response.json();
        console.log(data)
        setCategories(data); // Assuming the data is an array of categories
      } catch (error) {
        console.error("Error fetching categories:", error);
      }
    };

    fetchCategories();
  }, []);

  // Handle changes to form fields
  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement | any
    >
  ) => {
    const { name, value, type, checked, options } = e.target;

    if (type === "checkbox" || type === "radio") {
      setFormData((prevState) => ({
        ...prevState,
        [name]: checked ? value : "",
      }));
    } else if (type === "select-multiple") {
      const selectedOptions = Array.from(options)
        .filter((option: any) => option.selected)
        .map((option: any) => option.value);
      setFormData((prevState) => ({
        ...prevState,
        [name]: selectedOptions,
      }));
    } else {
      setFormData((prevState) => ({
        ...prevState,
        [name]: value,
      }));
    }
  };

  return (
    <div className="step-tab-panel step-tab-info active" id="tab_step1">
      <div className="tab-from-content">
        <div className="title-icon">
          <h3 className="title">
            <i className="uil uil-info-circle"></i> Basic Information
          </h3>
        </div>
        <div className="course__form">
          <div className="general_info10">
            <div className="row">
              <div className="col-lg-12 col-md-12">
                <div className="ui search focus mt-30 lbel25">
                  <label>Course Title*</label>
                  <div className="ui left icon input swdh19">
                    <input
                      className="prompt srch_explore"
                      type="text"
                      placeholder="Course title here"
                      name="title"
                      data-purpose="edit-course-title"
                      maxLength={60}
                      value={formData.title}
                      onChange={handleChange}
                    />
                    <div className="badge_num">60</div>
                  </div>
                  <div className="help-block">
                    (Please make this a maximum of 100 characters and unique.)
                  </div>
                </div>
              </div>

              <div className="col-lg-12 col-md-12">
                <div className="ui search focus lbel25 mt-30">
                  <label>Short Description*</label>
                  <div className="ui form swdh30">
                    <div className="field">
                      <textarea
                        rows={3}
                        name="description"
                        placeholder="Item description here..."
                        value={formData.description}
                        onChange={handleChange}
                      ></textarea>
                    </div>
                  </div>
                  <div className="help-block">220 words</div>
                </div>
              </div>

              <div className="col-lg-12 col-md-12">
                <div className="course_des_textarea mt-30 lbel25">
                  <label>Course Description*</label>
                  <div className="text-editor">
                    <textarea
                      className="form_textarea_1 ht-4"
                      placeholder="Item description here"
                      style={{ display: "none" }}
                    ></textarea>
                    <div id="editor1"></div>
                  </div>
                </div>
              </div>

              <div className="col-lg-6 col-md-12">
                <div className="ui search focus lbel25 mt-30">
                  <label>What will students learn in your course?*</label>
                  <div className="ui form swdh30">
                    <div className="field">
                      <textarea
                        rows={3}
                        name="whatStudentsLearn"
                        placeholder=""
                        value={formData.whatStudentsLearn}
                        onChange={handleChange}
                      ></textarea>
                    </div>
                  </div>
                  <div className="help-block">
                    Student will gain this skills, knowledge after completing
                    this course. (One per line).
                  </div>
                </div>
              </div>

              <div className="col-lg-6 col-md-12">
                <div className="ui search focus lbel25 mt-30">
                  <label>Requirements*</label>
                  <div className="ui form swdh30">
                    <div className="field">
                      <textarea
                        rows={3}
                        name="requirements"
                        placeholder=""
                        value={formData.requirements}
                        onChange={handleChange}
                      ></textarea>
                    </div>
                  </div>
                  <div className="help-block">
                    What knowledge, technology, tools required by users to start
                    this course. (One per line).
                  </div>
                </div>
              </div>

              <div className="col-lg-6 col-md-12">
                <div className="mt-30 lbel25">
                  <label>Course Level*</label>
                </div>
                <select
                  className="selectpicker"
                  multiple
                  data-selected-text-format="count > 3"
                  name="courseLevel"
                  value={formData.courseLevel}
                  onChange={handleChange}
                >
                  <option value="1">Beginner</option>
                  <option value="2">Intermediate</option>
                  <option value="3">Expert</option>
                </select>
              </div>

              <div className="col-lg-6 col-md-12">
                <div className="mt-30 lbel25">
                  <label>Audio Language*</label>
                </div>
                <select
                  className="selectpicker"
                  title="Select Audio"
                  multiple
                  data-selected-text-format="count > 4"
                  data-size="5"
                  name="audioLanguage"
                  value={formData.audioLanguage}
                  onChange={handleChange}
                >
                  <option>English</option>
                  <option>Español</option>
                  <option>Deutsch</option>
                  <option>Français</option>
                </select>
              </div>

              <div className="col-lg-6 col-md-6">
                <div className="mt-30 lbel25">
                  <label>Close Caption*</label>
                </div>
                <select
                  className="selectpicker"
                  title="Select Caption"
                  multiple
                  data-selected-text-format="count > 4"
                  data-size="5"
                  name="closeCaption"
                  value={formData.closeCaption}
                  onChange={handleChange}
                >
                  <option>English</option>
                  <option>Français</option>
                  <option>Polski</option>
                  <option>Tamil</option>
                  <option>Telugu</option>
                </select>
              </div>

              <div className="col-lg-6 col-md-6">
                <div className="mt-30 lbel25">
                  <label>Course Category*</label>
                </div>
                <select
                  className="selectpicker"
                  title="Select Category"
                  name="category"
                  id="selectcategory"
                  data-live-search="true"
                  value={formData.category}
                  onChange={handleChange}
                >
                  {categories.length > 0 ? (
                    categories.map((category) => (
                      <option key={category.id} value={category.id}>
                        {category.name}
                      </option>
                    ))
                  ) : (
                    <option disabled={true}>Loading categories...</option>
                  )}
                </select>
              </div>

            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CourseForm;
