import { useEffect, useState } from "react";
import { Link } from "react-router";

const API_URL = import.meta.env.VITE_API_URL || 'https://your-api-gateway-url.execute-api.us-east-1.amazonaws.com/prod';

const TOPICS = [
  { id: 'all', label: 'All Topics', icon: '🌐' },
  { id: 'defi', label: 'DeFi', icon: '💰' },
  { id: 'nft', label: 'NFTs', icon: '🎨' },
  { id: 'regulation', label: 'Regulation', icon: '⚖️' },
  { id: 'bitcoin', label: 'Bitcoin', icon: '₿' },
  { id: 'ethereum', label: 'Ethereum', icon: '◆' },
];

const FREQUENCIES = [
  { id: 'every_6_hours', label: 'Every 6 hours' },
  { id: 'daily', label: 'Once daily' },
  { id: 'twice_daily', label: 'Twice daily' },
];

export default function Preferences() {
  const [preferences, setPreferences] = useState({
    topics: ['all'],
    frequency: 'every_6_hours'
  });
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (typeof window !== 'undefined' && window.Telegram?.WebApp) {
      window.Telegram.WebApp.ready();
      window.Telegram.WebApp.expand();
    }

    // Fetch current preferences
    fetch(`${API_URL}/preferences`, {
      headers: {
        'X-Telegram-Init-Data': window.Telegram?.WebApp?.initData || ''
      }
    })
      .then(res => res.json())
      .then(data => {
        if (data.preferences) {
          setPreferences(data.preferences);
        }
      })
      .catch(err => console.error('Error fetching preferences:', err));
  }, []);

  const toggleTopic = (topicId: string) => {
    setPreferences(prev => {
      const topics = prev.topics.includes(topicId)
        ? prev.topics.filter(t => t !== topicId)
        : [...prev.topics, topicId];
      
      // Ensure at least one topic is selected
      return {
        ...prev,
        topics: topics.length > 0 ? topics : ['all']
      };
    });
  };

  const savePreferences = async () => {
    setSaving(true);
    
    try {
      await fetch(`${API_URL}/preferences`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Telegram-Init-Data': window.Telegram?.WebApp?.initData || ''
        },
        body: JSON.stringify({ preferences })
      });
      
      // Show success feedback
      if (window.Telegram?.WebApp) {
        window.Telegram.WebApp.showAlert('Preferences saved!');
      }
    } catch (err) {
      console.error('Error saving preferences:', err);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="container">
      <div className="header">
        <div className="logo">⚙️</div>
        <div className="header-text">
          <h1>Preferences</h1>
          <p>Customize your news feed</p>
        </div>
      </div>

      <div className="preferences-section">
        <div className="section-title">Topics</div>
        {TOPICS.map(topic => (
          <div key={topic.id} className="option">
            <div className="option-label">
              <span style={{ marginRight: '8px' }}>{topic.icon}</span>
              {topic.label}
            </div>
            <div 
              className={`toggle ${preferences.topics.includes(topic.id) ? 'active' : ''}`}
              onClick={() => toggleTopic(topic.id)}
            >
              <div className="toggle-thumb" />
            </div>
          </div>
        ))}
      </div>

      <div className="preferences-section">
        <div className="section-title">Frequency</div>
        {FREQUENCIES.map(freq => (
          <div 
            key={freq.id} 
            className="option"
            onClick={() => setPreferences(prev => ({ ...prev, frequency: freq.id }))}
          >
            <div className="option-label">{freq.label}</div>
            <div className={`toggle ${preferences.frequency === freq.id ? 'active' : ''}`}>
              <div className="toggle-thumb" />
            </div>
          </div>
        ))}
      </div>

      <button 
        className="save-button" 
        onClick={savePreferences}
        disabled={saving}
      >
        {saving ? 'Saving...' : 'Save Preferences'}
      </button>

      <nav className="nav">
        <Link to="/" className="nav-item">
          <div className="nav-icon">📰</div>
          <div>Briefs</div>
        </Link>
        <Link to="/preferences" className="nav-item active">
          <div className="nav-icon">⚙️</div>
          <div>Settings</div>
        </Link>
      </nav>
    </div>
  );
}
