import React from 'react';
import { Link } from 'react-router-dom';
import { FaGraduationCap, FaFileAlt, FaRedoAlt, FaFileUpload, FaHeadset } from 'react-icons/fa';
import '../static/css/LandingPage.css';

const Home = () => {
  const helpCards = [
    {
      id: 1,
      icon: <FaFileAlt />,
      title: 'Report an issue',
      description: 'Report a problem of missing marks, wrong marks, or other academic issues',
      link: '/add-issue'
    },
    {
      id: 2,
      icon: <FaRedoAlt />,
      title: 'Ask for Re-do',
      description: 'Request your lecturer to repeat a failed or missed paper',
      link: '/add-issue'
    },
    {
      id: 3,
      icon: <FaFileUpload />,
      title: 'Submit a document',
      description: 'Submit a document for review, including essays, papers, or other written assignments',
      link: '/add-issue'
    },
    {
      id: 4,
      icon: <FaHeadset />,
      title: 'Get support',
      description: 'Get help with a technical issue or other problem not related to your course or academic experience',
      link: '/support'
    }
  ];

  return (
    <div className="landing-page">
      <nav className="top-nav">
        <div className="nav-logo">
          <Link to="/">
            <FaGraduationCap className="logo-icon" />
            <span>AITs</span>
          </Link>
        </div>
        <div className="nav-profile">
          <Link to="/profile">
            <img src="/profile-placeholder.png" alt="Profile" />
          </Link>
        </div>
      </nav>

      <main className="main-content">
        <section className="hero-section">
          <div className="hero-content">
            <h1>Welcome to AITS</h1>
            <p>Report any academic issues</p>
            <div className="hero-buttons">
              <Link to="/login" className="btn btn-primary">Sign in</Link>
              <Link to="/signup" className="btn btn-secondary">Sign up</Link>
            </div>
          </div>
        </section>

        <section className="help-section">
          <h2>How can we help you?</h2>
          <div className="help-cards">
            {helpCards.map(card => (
              <Link to={card.link} key={card.id} className="help-card">
                <div className="card-icon">
                  {card.icon}
                </div>
                <h3>{card.title}</h3>
                <p>{card.description}</p>
              </Link>
            ))}
          </div>
        </section>

        <section className="contact-section">
          <h2>Need help? We're here for you</h2>
          <div className="contact-info">
            <div className="contact-item">
              <h3>Phone</h3>
              <p>(+256)776622594</p>
              <p className="subtitle">Monday - Friday: 9AM - 5PM</p>
            </div>
            <div className="contact-item">
              <h3>FAQs</h3>
              <p>Find answers to common questions</p>
              <Link to="/faqs" className="link-text">View FAQs</Link>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
};

export default Home
