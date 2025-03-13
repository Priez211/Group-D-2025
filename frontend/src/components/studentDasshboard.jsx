import React from "react";
import {Link} from "react-router-dom";
import {FaHome, FaPlusCircle, FaBell, FaCog} from "react-icons/fa";
import "../static/css/studentsDashboard.css";

const studentsDashboard = () => {
    const recentIssues = [
        {id: 1, title:"missing marks", description:"im missing coursework marks",date:"Mar 2, 2024", status:"pending", colour:"#92A8D1"},
        {id:2, title:"requesting for a re-do", description:"i want to re-sit the previous test", date:"feb 25,2024", status:"approved",colour:"#E6E6E6"},
        {id: 3, title:"wrong marks", description:"the marks im having are not the ones i got in exams", date:"Feb 25, 2025", status:"pending", colour:"#88D8B0"}
    ];
    return (
        <div className= "dashboard-page">
            <nav className = "top-nav">
                <div className = "nav-logo">
                    <Link to = "/">
                    <img src="/graduation-cap.png" alt= "AiTs Logo" className="logo-icon"/>
                    <span>AiTs</span>
                    </Link>
                </div>
                <div className = "nav-profile">
                    <Link to = "/profile">
                        <img src="/profile-placeholde.png" alt = "Profile"/>
                    </Link>
                </div>
            </nav>
            <aside className= "sidebar">
                <nav className= "side_nav">
                    <Link to= "/studentsDashboard" className="nav-item active">
                        <FaHome/>
                        <span>Home</span>
                    </Link>
                    <Link to ="/add-issue" className= "nav-item">
                        <FaPlusCircle/>
                        <span>Add New Issue</span>
                    </Link>
                    <Link to= "/notifications" className= "nav-item">
                        <FaBell/>
                        <span>Notifications</span>
                    </Link>
                    <Link to="/settings" className = "nav-item">
                    </Link>
                </nav>
            </aside>
            <main className= "main-content">
                <div className= "welcome-section">
                    <h1> welcome back to AiTs</h1>
                </div>
                <section className= "recent-issues">
                    <h2> Recent issues</h2>
                    <div className = "issues-list">
                        {recentIssues.map(issue => (
                            <div key={issue.id} className="issue-card">
                                <div className="issue-icon" style={{ backgroundColor: issue.colour }}></div><div className="issue-content"></div>
                                <div className = "issue-content">
                                    <h3>{issue.title}</h3>
                                    <p> {issue.description}</p>
                                </div>
                                <div className= "issue-date">{issue.date}</div>
                                </div>
                        ))}
                    </div>
                    <Link to= "/add-issue" className= "add-issue-button">
                        <FaPlusCircle/>
                        Add New Issue
                    </Link>
                </section>
            </main>

        </div>
    );
};
export default studentsDashboard;
