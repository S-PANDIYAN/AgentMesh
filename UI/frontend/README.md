# AgentMesh Frontend Structure

Professional, organized, scalable frontend for the AgentMesh Intelligence Hub.

## 📁 Directory Structure

```
frontend/
├── public/                    # Production-ready files
│   ├── index.html            # Dashboard/Home page
│   ├── pr-review.html        # PR Review Summary page
│   ├── agent-analysis.html   # Agent Analysis page
│   ├── hot-reload.html       # Hot Reload State page
│   ├── base.html             # Base template
│   └── styles.css            # Compiled Tailwind CSS (generated)
│
├── src/
│   ├── components/           # Reusable HTML components
│   │   ├── header.html       # Top navigation bar
│   │   ├── sidebar.html      # Left sidebar navigation
│   │   └── footer.html       # Bottom navigation bar
│   │
│   ├── js/
│   │   ├── api.js            # REST API integration module
│   │   └── utils.js          # Utility functions
│   │
│   ├── styles/
│   │   └── input.css         # Tailwind CSS input (compiled to public/styles.css)
│   │
│   └── assets/               # Images, icons, etc.
│
├── package.json              # NPM dependencies and scripts
├── tailwind.config.js        # Tailwind CSS configuration
└── README.md                 # This file
```

## 🚀 Getting Started

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
# Watch mode - compiles Tailwind CSS on changes
npm run watch

# Dev server (in another terminal)
npm run dev
```

Visit `http://localhost:8080`

### Production Build

```bash
npm run build
```

## 🔧 Component System

### Header Component (`src/components/header.html`)
- Fixed top navigation
- Brand logo
- Menu links
- Action buttons (notifications, settings, terminal)
- User avatar

**Usage:**
Load into any page with the component loader script:
```javascript
loadComponent('header-container', 'header.html');
```

### Sidebar Component (`src/components/sidebar.html`)
- Fixed left navigation
- Cluster status display
- Menu items with icons
- "Deploy Agent" button
- Active state management

### Footer Component (`src/components/footer.html`)
- Fixed bottom dock
- Tab navigation (Live Logs, Metrics, Diagnostics, Terminal)
- Status badges

## 📄 Pages

### `public/index.html` - Dashboard
Main entry point showing:
- Welcome section
- File upload dropzone
- Quick stats (Active Agents, API Status)
- Recent analyses list

### `public/pr-review.html` - PR Review Summary
Detailed analysis results showing:
- PR header with confidence score
- Bento grid (Safety Score, Critical Issues, Status)
- Agent findings table
- Swarm recommendations
- System impact metrics
- Action buttons (Export, Re-scan, Approve)

### `public/agent-analysis.html` - Agent Analysis
Individual agent deep-dive showing:
- Single agent metrics
- Detailed findings with code references
- Confidence breakdown
- Recommendations

### `public/hot-reload.html` - Hot Reload State
System recalibration status showing:
- Recalibration progress
- Agent reload status
- System health indicators

## 🔗 API Integration

All API calls are handled through `src/js/api.js`:

```javascript
// Check API health
await AgentMeshAPI.checkHealth();

// Get available agents
await AgentMeshAPI.getAgents();

// Submit code for review
await AgentMeshAPI.submitReview(filePath, code, agents, priority);

// Get task status
await AgentMeshAPI.getTaskStatus(taskId);

// Poll until completion
await AgentMeshAPI.pollTaskStatus(taskId);

// Reload agents
await AgentMeshAPI.reloadAgents();
```

## 🎨 Styling

### Tailwind CSS
- Configuration: `tailwind.config.js`
- Input file: `src/styles/input.css`
- Output: `public/styles.css`

### Custom Colors
All colors defined in `tailwind.config.js`:
- Primary: `#735c00` (Brown)
- Primary Container: `#facc15` (Yellow)
- Background: `#fff8f3` (Off-white)
- Surface: `#fff8f3`
- And 40+ more semantic colors

### Custom Fonts
- **Headline**: Space Grotesk (bold, tracking)
- **Body**: Inter (readable, clean)
- **Label**: Space Grotesk

## 🔌 Connecting to AgentMesh API

1. Ensure your REST API is running:
   ```bash
   python api/rest_api.py  # or agentmesh-server
   ```

2. Update API endpoint in `src/js/api.js` if needed:
   ```javascript
   const API_BASE = 'http://localhost:5000';
   ```

3. Features automatically enabled:
   - Health checks
   - Agent listing
   - Code review submission
   - Task status polling
   - Real-time updates

## 📱 Responsive Design

- **Mobile**: Sidebar hidden, full-width main content
- **Tablet**: Sidebar togglable, optimized layout
- **Desktop**: Full 3-column layout (sidebar, content, utilities)

## ♿ Accessibility

- ARIA labels on all interactive elements
- Semantic HTML structure
- Keyboard navigation support
- Color contrast meets WCAG AA standards
- Material symbols for icon accessibility

## 🚢 Deployment

### Using Python Live Server
```bash
cd public
python -m http.server 8000
```

### Using Node.js
```bash
npx serve public
```

### Docker
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npx", "serve", "public"]
```

## 🐛 Troubleshooting

**Components not loading:**
- Check that component files exist in `src/components/`
- Verify fetch paths in HTML
- Check browser console for CORS errors

**Styles not applied:**
- Run `npm run build` to compile Tailwind
- Clear browser cache (Ctrl+Shift+Delete)
- Verify `styles.css` exists in `public/`

**API errors:**
- Ensure REST API server is running
- Check API endpoint URL in `api.js`
- Verify CORS is enabled in backend

## 📦 Dependencies

- **tailwindcss**: ^3.3.0 - Utility-first CSS framework
- **live-server**: ^1.2.2 - Development server (optional)

## 🎯 Next Steps

1. ✅ Build and deploy frontend
2. ✅ Connect to REST API
3. Add dark mode toggle
4. Add user preferences/settings
5. Add analytics dashboard
6. Add webhook integration for GitHub
7. Add real-time WebSocket updates
8. Add multi-file batch analysis

## 📞 Support

For issues or questions:
- Check browser Console (F12)
- Verify API server is running
- Review `src/js/api.js` for endpoint definitions
- Check `tailwind.config.js` for style issues
