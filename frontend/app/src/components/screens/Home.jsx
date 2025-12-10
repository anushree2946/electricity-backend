import React, { useState, useEffect } from "react";
import axios from "axios";
import API_BASE_URL from "../../api";
import { Row, Col } from "react-bootstrap";
import { Link } from "react-router-dom";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import "./Home.css";

function Home() {
  const [data, setData] = useState([]);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [loading, setLoading] = useState(false);

  // Redirect if not logged in
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) window.location.href = "/login";
  }, []);

  // Fetch Data whenever filters/page changes
  useEffect(() => {
    fetchData();
  }, [currentPage, startDate, endDate, searchQuery]);

  const fetchData = async () => {
    try {
      setLoading(true);

      const token = localStorage.getItem("token");
      if (!token) {
        window.location.href = "/login";
        return;
      }

      let url = `${API_BASE_URL}/api/getApplicantsData/?page=${currentPage}`;

      if (startDate && endDate) {
        url += `&start_date=${startDate.toISOString().split("T")[0]}&end_date=${endDate
          .toISOString()
          .split("T")[0]}`;
      }

      if (searchQuery.trim()) {
        url += `&search=${encodeURIComponent(searchQuery.trim())}`;
      }

      const res = await axios.get(url, {
        headers: { Authorization: `Bearer ${token}` },
      });

      setData(res.data.data || []);
      setTotalPages(res.data.total_pages || 1);
    } catch (error) {
      console.error("Fetch Error:", error);

      if (error.response?.status === 401) {
        localStorage.removeItem("token");
        window.location.href = "/login";
      }
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/login";
  };

  return (
    <div className="container mt-2">
      <div className="d-flex justify-content-between align-items-center">
        <h1>Applicant Details</h1>
        <button className="btn btn-danger" onClick={handleLogout}>
          Logout
        </button>
      </div>

      <hr />

      <Row>
        <p>Filter By Date of Application</p>

        <Col md={2}>
          <DatePicker
            selected={startDate}
            className="form-control date"
            onChange={setStartDate}
            placeholderText="From Date"
          />
        </Col>

        <Col md={2}>
          <DatePicker
            selected={endDate}
            className="form-control date"
            onChange={setEndDate}
            placeholderText="To Date"
          />
        </Col>

        <Col md={3}></Col>

        <Col md={5}>
          <input
            type="text"
            className="form-control"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search By Applicant ID.."
          />
        </Col>
      </Row>

      <hr />

      <div className="table-container">
        {loading ? (
          <p className="text-center">Loading data...</p>
        ) : (
          <table className="table table-bordered">
            <thead className="sticky-header">
              <tr>
                <th>ID</th>
                <th>Applicant Name</th>
                <th>Gender</th>
                <th>District</th>
                <th>State</th>
                <th>Pincode</th>
                <th>Load Applied</th>
                <th>Date of Application</th>
                <th>Status</th>
                <th>Reviewer Name</th>
                <th>Edit</th>
              </tr>
            </thead>

            <tbody>
              {data.length > 0 ? (
                data.map((connection) => (
                  <tr key={connection.id}>
                    <td>{connection.id}</td>
                    <td>{connection.Applicant?.Applicant_Name || "-"}</td>
                    <td>{connection.Applicant?.Gender || "-"}</td>
                    <td>{connection.Applicant?.District || "-"}</td>
                    <td>{connection.Applicant?.State || "-"}</td>
                    <td>{connection.Applicant?.Pincode || "-"}</td>
                    <td>{connection.Load_Applied}</td>
                    <td>{connection.Date_of_Application}</td>
                    <td>{connection.Status}</td>
                    <td>{connection.Reviewer_Name || "-"}</td>

                    <td>
                      <Link
                        to={`/editApplicant/${connection.id}`}
                        className="btn btn-outline-success btn-sm"
                      >
                        Edit
                      </Link>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="11" className="text-center">
                    No data available
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        )}
      </div>

      {/* PAGINATION BLOCK (important) */}
      <div className="container mt-3">
        <ul className="pagination justify-content-center">

          {/* First Page */}
          <li className={`page-item ${currentPage === 1 ? "disabled" : ""}`}>
            <button onClick={() => setCurrentPage(1)} className="page-link">
              First
            </button>
          </li>

          {/* Page Numbers */}
          {Array.from({ length: totalPages }).map((_, index) => (
            <li
              key={index}
              className={`page-item ${currentPage === index + 1 ? "active" : ""}`}
            >
              <button
                onClick={() => setCurrentPage(index + 1)}
                className="page-link"
              >
                {index + 1}
              </button>
            </li>
          ))}

          {/* Last Page */}
          <li className={`page-item ${currentPage === totalPages ? "disabled" : ""}`}>
            <button
              onClick={() => setCurrentPage(totalPages)}
              className="page-link"
            >
              Last
            </button>
          </li>

        </ul>
      </div>
    </div>
  );
}

export default Home;
