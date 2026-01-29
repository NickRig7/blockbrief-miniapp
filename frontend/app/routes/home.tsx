import { useEffect, useState } from "react";
import { Link } from "react-router";

const API_URL = import.meta.env.VITE_API_URL || 'https://your-api-gateway-url.execute-api.us-east-1.amazonaws.com/prod';

interface Story {
  storyId: string;
  title: string;
  summary: string;
  url: string;
  source: string;
  imageUrl?: string;
}

interface Brief {
  briefId: string;
  stories: Story[];
  publishedAt: number;
  storyCount: number;
}

export default function Home() {
  const [briefs, setBriefs] = useState<Brief[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Initialize Telegram WebApp
    if (typeof window !== 'undefined' && window.Telegram?.WebApp) {
      window.Telegram.WebApp.ready();
      window.Telegram.WebApp.expand();
    }

    // Fetch briefs
    fetch(`${API_URL}/briefs`)
      .then(res => res.json())
      .then(data => {
        setBriefs(data.briefs || []);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching briefs:', err);
        setLoading(false);
      });
  }, []);

  const formatTime = (timestamp: number) => {
    const date = new Date(timestamp * 1000);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const hours = Math.floor(diff / (1000 * 60 * 60));
    
    if (hours < 1) return 'Just now';
    if (hours < 24) return `${hours}h ago`;
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  if (loading) {
    return (
      <div className="container">
        <div className="header">
          <div className="logo">📰</div>
          <div className="header-text">
            <h1>BlockBrief</h1>
            <p>AI-Curated Crypto News</p>
          </div>
        </div>
        <div className="loading">Loading latest briefs...</div>
        <Navigation />
      </div>
    );
  }

  if (briefs.length === 0) {
    return (
      <div className="container">
        <div className="header">
          <div className="logo">📰</div>
          <div className="header-text">
            <h1>BlockBrief</h1>
            <p>AI-Curated Crypto News</p>
          </div>
        </div>
        <div className="empty">
          <div className="empty-icon">🤖</div>
          <div className="empty-text">
            Your AI Editor-in-Chief is preparing the first brief.
            <br />Check back in a few minutes!
          </div>
        </div>
        <Navigation />
      </div>
    );
  }

  return (
    <div className="container">
      <div className="header">
        <div className="logo">📰</div>
        <div className="header-text">
          <h1>BlockBrief</h1>
          <p>AI-Curated Crypto News</p>
        </div>
      </div>

      {briefs.map((brief) => (
        <div key={brief.briefId} className="brief-card">
          <div className="brief-header">
            <div className="brief-time">
              {formatTime(brief.publishedAt)}
            </div>
          </div>

          {brief.stories.map((story, index) => (
            <div key={story.storyId} className="story">
              <div className="story-number">{index + 1}</div>
              <div className="story-title">{story.title}</div>
              <div className="story-summary">{story.summary}</div>
              <div className="story-meta">
                <a 
                  href={story.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="story-link"
                  onClick={() => {
                    if (window.Telegram?.WebApp) {
                      window.Telegram.WebApp.openLink(story.url);
                    }
                  }}
                >
                  Read more →
                </a>
                <span>•</span>
                <span>{story.source}</span>
              </div>
            </div>
          ))}
        </div>
      ))}

      <Navigation />
    </div>
  );
}

function Navigation() {
  return (
    <nav className="nav">
      <Link to="/" className="nav-item active">
        <div className="nav-icon">📰</div>
        <div>Briefs</div>
      </Link>
      <Link to="/preferences" className="nav-item">
        <div className="nav-icon">⚙️</div>
        <div>Settings</div>
      </Link>
    </nav>
  );
}

declare global {
  interface Window {
    Telegram?: {
      WebApp: {
        ready: () => void;
        expand: () => void;
        openLink: (url: string) => void;
        initData: string;
      };
    };
  }
}
