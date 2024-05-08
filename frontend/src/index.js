/*!

=========================================================
* Now UI Kit PRO React - v1.5.2
=========================================================

* Product Page: https://www.creative-tim.com/product/now-ui-kit-pro-react
* Copyright 2023 Creative Tim (http://www.creative-tim.com)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Route, Navigate, Routes } from "react-router-dom";

// styles
import "assets/css/bootstrap.min.css";
import "assets/scss/now-ui-kit.scss?v=1.5.0";
import "assets/demo/demo.css?v=1.5.0";
import "assets/demo/react-demo.css?v=1.5.0";
import "assets/demo/nucleo-icons-page-styles.css?v=1.5.0";
// pages
import AboutUs from "views/examples/AboutUs.js";
import BlogPost from "views/examples/BlogPost.js";
import BlogPosts from "views/examples/BlogPosts.js";
import ContactUs from "views/examples/ContactUs.js";
import Ecommerce from "views/examples/Ecommerce.js";
import Index from "views/Index.js";
import LandingPage from "views/examples/LandingPage.js";
import LoginPage from "views/examples/LoginPage.js";
import NucleoIcons from "views/NucleoIcons.js";
import Presentation from "views/Presentation.js";
import Pricing from "views/examples/Pricing.js";
import ProductPage from "views/examples/ProductPage.js";
import ProfilePage from "views/examples/ProfilePage.js";
import Sections from "views/Sections.js";
import SignupPage from "views/examples/SignupPage.js";
import Test from "views/test.js";
import Tool from "views/tool.js";
import Tool_File from "views/tool_file.js";
import Rag from "views/rag.js";
// others

const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <BrowserRouter>
    <Routes>
      <Route path="/about-us" element={<AboutUs />} />
      <Route path="/blog-post" element={<BlogPost />} />
      <Route path="/blog-posts" element={<BlogPosts />} />
      <Route path="/contact-us" element={<ContactUs />} />
      <Route path="/e-commerce" element={<Ecommerce />} />
      <Route path="/index" element={<Index />} />
      <Route path="/landing-page" element={<LandingPage />} />
      <Route path="/login-page" element={<LoginPage />} />
      <Route path="/nucleo-icons" element={<NucleoIcons />} />
      <Route path="/presentation" element={<Presentation />} />
      <Route path="/pricing" element={<Pricing />} />
      <Route path="/product-page" element={<ProductPage />} />
      <Route path="/profile-page" element={<ProfilePage />} />
      <Route path="/sections" element={<Sections />} />
      <Route path="/sign-up" element={<SignupPage />} />
      <Route path="/test" element={<Test />} />
      <Route path="/tool" element={<Tool />} />
      <Route path="/toolfile" element={<Tool_File />} />
      <Route path="/rag" element={<Rag />} />
      <Route path="*" element={<Navigate to="/presentation" replace />} />
    </Routes>
  </BrowserRouter>
);
