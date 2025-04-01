

<h1> Project</h1>

<div class="layout">
	<!-- Sidebar -->
	<aside class="sidebar">
		<div class="user-info">
			<div class="initials-circle">{initials}</div>
			<div class="role">{role}</div>
		</div>

        <div class="sidebar-icons">
			<div class="sidebar-section">
				<button
					class:active-icon={active === "projects"}
					on:click={() => (active = "projects")}
					title="Projects"
				>
					<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12.75V12A2.25 2.25 0 0 1 4.5 9.75h15A2.25 2.25 0 0 1 21.75 12v.75m-8.69-6.44-2.12-2.12a1.5 1.5 0 0 0-1.061-.44H4.5A2.25 2.25 0 0 0 2.25 6v12a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9a2.25 2.25 0 0 0-2.25-2.25h-5.379a1.5 1.5 0 0 1-1.06-.44Z" />
					</svg>
					<span class="icon-label">Projects</span>
				</button>
			</div>

			{#if role === "Lead"}
				<div class="sidebar-section">
					<button
						class:active-icon={active === "delete"}
						on:click={() => (active = "delete")}
						title="Delete Project"
					>
						<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
						</svg>
						<span class="icon-label">Delete Project</span>
					</button>
				</div>
			{/if}
      <!--Setting  Container  -->
			<div class="settings">
				<button
					class:active-icon={active === "settings"}
					on:click={() => showSettings = true}
					title="Settings"
				>
					<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" d="M11.42 15.17 17.25 21A2.652 2.652 0 0 0 21 17.25l-5.877-5.877M11.42 15.17l2.496-3.03c.317-.384.74-.626 1.208-.766M11.42 15.17l-4.655 5.653a2.548 2.548 0 1 1-3.586-3.586l6.837-5.63m5.108-.233c.55-.164 1.163-.188 1.743-.14a4.5 4.5 0 0 0 4.486-6.336l-3.276 3.277a3.004 3.004 0 0 1-2.25-2.25l3.276-3.276a4.5 4.5 0 0 0-6.336 4.486c.091 1.076-.071 2.264-.904 2.95l-.102.085m-1.745 1.437L5.909 7.5H4.5L2.25 3.75l1.5-1.5L7.5 4.5v1.409l4.26 4.26m-1.745 1.437 1.745-1.437m6.615 8.206L15.75 15.75M4.867 19.125h.008v.008h-.008v-.008Z" />
					</svg>
					<span class="icon-label">Settings</span>
				</button>
			</div>
		</div>

		<!-- Logout Container-->
		<div class="logout-wrapper">
			<button class="logout" on:click={logout}>Log Out</button>
		</div>
	</aside>
    <!-- Main Content -->
	<main class="main">
		<header class="header"></header>
	</main>
  <SettingsPopup open={showSettings} onClose={() => showSettings = false} />
</div>

<style>
	.layout {
		display: flex;
		min-height: 100vh;
		font-family: "Raleway", sans-serif;
		background: #f9f9f9;
	}

	.sidebar {
		width: 80px;
		background: linear-gradient(to bottom, #000000, #0f172a);
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 1rem 0;
		border-top-right-radius: 10px;
		border-bottom-right-radius: 10px;
		color: #fff;
		box-shadow: 2px 0 6px rgba(0, 0, 0, 0.05);
	}

	.user-info {
		text-align: center;
		font-size: 0.75rem;
		margin-bottom: 2rem;
		color: #cbd5e1;
	}

	.initials-circle {
		width: 36px;
		height: 36px;
		border-radius: 50%;
		background-color: #334155;
		color: white;
		display: flex;
		align-items: center;
		justify-content: center;
		font-weight: bold;
		margin: 0 auto 0.25rem;
	}

	.sidebar-icons {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
		align-items: center;
		flex-grow: 1;
		justify-content: center;
		width: 100%;
	}

	.sidebar-section button,
	.settings button {
		background: none;
		border: none;
		cursor: pointer;
		transition: transform 0.2s ease, background 0.2s;
		padding: 0.75rem;
		border-radius: 12px;
		display: flex;
		align-items: center;
		justify-content: center;
		position: relative;
		flex-direction: column;
	}

	.sidebar-section button:hover,
	.settings button:hover {
		transform: scale(1.3);
		background: rgba(255, 255, 255, 0.12);
	}

	.active-icon {
		background: rgba(255, 255, 255, 0.2);
	}

	svg {
		width: 32px;
		height: 32px;
		stroke: #cbd5e1;
	}

	.icon-label {
		font-size: 0.8rem;
		margin-top: 0.5rem;
		color: #cbd5e1;
		display: block;
	}

	.logout-wrapper {
		margin-top: auto;
		padding-bottom: 1rem;
		width: 100%;
		display: flex;
		justify-content: center;
	}

  .logout {
    padding: 0.5rem 1rem;
    background: #334155;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
    font-size: 0.75rem;
    width: 90%;
    text-align: center;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  }

  .logout:hover {
    background: #1e293b;
    transform: translateY(-3px) scale(1.05);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
  }

	.logout:hover {
		background: #1e293b;
	}

	.main {
		flex: 1;
		padding: 2rem;
	}

	.header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-bottom: 2rem;
	}
</style>