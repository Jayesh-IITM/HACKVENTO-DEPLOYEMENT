// Configure the backend API base for the portal pages.
// Goal: portal pages must call the BACKEND service URL, not the frontend URL.
//
// Priority order:
// 1) window.API_BASE (explicit override)
// 2) localStorage.API_BASE (persisted override)
// 3) Guess backend from frontend hostname ("...portal..." -> "...backend...")
// 4) Local dev fallback

(function () {
	const isLocal =
		window.location.hostname === "localhost" ||
		window.location.hostname === "127.0.0.1";

	const persisted = (() => {
		try {
			return localStorage.getItem("API_BASE") || "";
		} catch {
			return "";
		}
	})();

	const guessBackendBase = () => {
		const host = window.location.hostname;

		// Common Railway naming: *-portal.* -> *-backend.*
		if (host.includes("portal")) {
			const guessedHost = host
				.replace("-portal", "-backend")
				.replace("portal", "backend");
			return `https://${guessedHost}/api`;
		}

		// Fallback: Render backend (current deployment)
		// Update this if your Render service domain changes
		return "https://hackvento-deployement.onrender.com/api";
	};

	const defaultBase = isLocal ? "http://localhost:5000/api" : guessBackendBase();

	// Allow explicit override via window.API_BASE before this file runs.
	window.API_BASE = window.API_BASE || persisted || defaultBase;

	// Helpful debug
	console.log("🔗 Portal API_BASE:", window.API_BASE);
})();
