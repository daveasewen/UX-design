# Claude Docs in every session: what it is and how to turn it off

Sub-report 298-A · research lane · filed 2026-09-23 · for Dave and the conductor
Question: "Claude Docs" (tools mcp__Claude_Docs__*) arrives in every new session. Removing it in the Claude desktop app (macOS, v2.7032.0) fails with the toast "Failed to remove server". Can it be switched off for good?

---

## The answer

**Claude Docs is not a connector you added.** It is one of Anthropic's own features, a document type like Claude Design and Claude Slides. So the Remove button on the connector list is not the way to turn it off.

**The documented off switch is Settings > Capabilities.** Anthropic's Help Center says Docs is "on by default on Pro, Max, and Team plans, and you can turn it off in Settings > Capabilities". On an Enterprise seat only an organisation Owner can switch it, in Organization settings > Artifacts.

**No source says the switch stops the tools loading in new Claude Code or cloud sessions.** That is the part Dave cares about, and it has to be tested: switch it off, open a new session, and check whether the Claude Docs tools are still there.

**The "Failed to remove server" error has been reported before, for a different server.** It is a public, unresolved bug report about another server Anthropic adds automatically ("Claude Code Remote"). No source mentions Claude Docs with this error, and Anthropic has not replied on that thread.

---

## 1. What Claude Docs is (sourced)

- **Launched 16 September 2026, in beta.** It launched with Claude Slides on the same day that Cowork and chat merged. It is "in beta on paid plans, and Enterprise admins choose when to turn them on". Source: claude.com/blog/cowork-is-now-claude
- **It is an artifact feature, not a connector.** The Help Center lists Claude Design, Claude Slides and Claude Docs as the three artifact tools ("Create designs, decks, and docs"). Every doc is "saved in the Artifacts tab". Sources: support.claude.com articles 9487310 and 16923645.
- **It is meant to reach every surface, Claude Code included.** In the Help Center's words: "Claude Code: Ask Claude to turn the session you're in into a spec, runbook, or readout. On desktop, the doc opens in the side panel." It can also be started with /docs, or with "Output" then "Docs" in the message box. Source: 16923645.
- **Plans.** Pro, Max, Team and Enterprise have it; Free does not. It is not available yet for organisations using CMEK, ZDR or a HIPAA-ready configuration. Source: 16923645.
- **Watch the name.** Anthropic's documentation site at claude.com/docs is also called "Claude Docs" (for example, "Claude Docs: Connectors" in article 11176164). That site is unrelated to the Docs feature, so searches return a mix of both.

## 2. Every supported way to turn it off (sourced, exact labels where given)

1. **Your own account (Pro, Max, Team): Settings > Capabilities.** Quote: "It's on by default on Pro, Max, and Team plans, and you can turn it off in Settings > Capabilities." The source does not name the switch on that page. By analogy with Design it is probably labelled "Docs" or "Claude Docs", but that is an inference. Source: 16923645.
2. **Organisation owner (Team or Enterprise): Organization settings > Artifacts > Docs.** Quote: "Go to Organization settings > Artifacts. Turn on Docs." The Claude Design admin guide confirms that "Claude Slides and Claude Docs have their own settings on the same page, Slides and Docs". On Enterprise it is off until an Owner turns it on. "Claude Docs needs artifacts to be on for your organization." Sources: 16923645 and 14604406.
3. **Enterprise custom roles.** "you can turn on Claude Docs for specific groups … using the Docs capability (under Artifacts) in custom roles." Source: 16923645.
4. **Per-chat connector switches (+ > Connectors).** These exist for connectors: "Enable the specific services you want Claude to use for that conversation by toggling them on". No source says Claude Docs appears in that list. Source: 11176164.
5. **Per-thread switch in claude.ai/code cloud sessions.** "open the thread and select Connectors from the + menu beside its message box. Turning a connector off there removes it from that thread and saves that as your account default, so new threads and claude.ai chats start without it." This is the only documented switch that carries over to new sessions. Again, no source says Docs is listed there. The desktop docs add that "The + button is not available in cloud or WSL sessions" in the desktop app's Code tab, so this switch is on the web at claude.ai/code. Sources: code.claude.com/docs/en/claude-projects and code.claude.com/docs/en/desktop.
6. **Customize > Connectors > Remove.** This is the documented way to remove a connector you added: "Go to Customize > Connectors … Click 'Remove' or select the three-dot menu." Docs is not such a connector, so this is not a documented way to turn off Docs. Sources: claude.com/docs/connectors/custom/remote-mcp and 11176164.
7. **Claude Code settings do not reach it.** `disableClaudeAiConnectors` and `ENABLE_CLAUDEAI_MCP_SERVERS` "act only on … the connectors Claude Code fetches itself", which covers terminal, IDE and SDK sessions. In cloud sessions "The cloud host passes them in", governed by "Your claude.ai organization settings" plus admin allow and deny lists. In the desktop app's local sessions "no MCP setting or managed-mcp.json reaches them". Source: code.claude.com/docs/en/mcp ("How connectors reach Claude Code"). These settings are documented for claude.ai connectors only; Docs is not described as one.

## 3. The "Failed to remove server" toast (sourced, and what is missing)

- **The same error is on a public bug report.** GitHub anthropics/claude-ai-mcp issue #509, "cannot remove claude code remote custom connector". A server Anthropic added automatically ("Claude Code Remote") appeared in users' connector lists. Removing it showed "failed to remove server", and one user later saw "Server not found" after refreshing. Several users confirmed it; one said it was fixed, then that it came back. No Anthropic reply or fix is visible on the thread. Source: github.com/anthropics/claude-ai-mcp/issues/509
- **It is not in the release notes.** The desktop release notes for Dave's exact version (v2.7032.0, 22 Sep 2026) have no entry about Claude Docs or this error. Neither do the Help Center release notes up to 22 Sep. Sources: claude.com/docs/cowork/changelog and support.claude.com article 12138966.
- **No source addresses Claude Docs and this error together.** No source says the toast is the intended reply to removing a built-in feature, and no source offers a workaround for Docs.

## 4. Does switching it off change what a new session loads? (no source)

No source says. The Help Center describes the switch in terms of creating docs, not in terms of tools loading into Claude Code or cloud sessions. A related request on GitHub says built-in servers "load their tool names and instructions into every session's initial context even when unused". That request names claude-in-chrome, computer-use, mcp-registry and scheduled-tasks, not Docs. It shows the general problem is known, but it does not answer this question. Source: github.com/anthropics/claude-code/issues/82498.

---

## Observed in this research session (first-hand, not a public source)

- **This session started with Claude Docs attached.** It was a cloud session linked to Dave's Mac and attached to the Apollo Project. It started with an MCP server named "Claude_Docs" and that server's instructions, with the same tools Dave lists. The Artifact tool's own description here refers to "a first-party document connector (host-designated)". That suggests the app itself classes Docs as a built-in, first-party server, not a user connector.
- **Mid-run the app reported "Claude_Docs" as disconnected.** This happened between about 11:15 and 11:24 BST on 23 Sep. The cause is unknown. If Dave changed a setting around then, that timing is a useful clue. It could also have been a brief server outage.

## Inferred, not sourced

- **Why the tools arrived when the connectors panel said Docs was "not connected".** The connector list shows only connectors. The Docs server is probably attached because the Docs feature is switched on under Capabilities, whatever the connector list says.
- **Why "Failed to remove server" appears.** The Remove action most likely tries to delete a connector that belongs to Anthropic, and the server refuses. This matches the pattern in issue #509. The toast is probably a real failure with a poor message, not a deliberate "you can't remove this" reply.
- **The likely lasting fix.** If the Capabilities switch also controls whether Docs is attached to sessions, switching it off should keep Docs out of new sessions. That has to be tested.
- **If Dave's gmail account is a seat in a work Enterprise organisation,** his own Settings > Capabilities page may not show the switch. The organisation Owner then controls it at Organization settings > Artifacts > Docs.

## Next step for Dave (a test, one sitting)

1. Open Claude on the web or in the desktop app. Go to Settings > Capabilities and switch off Claude Docs. If there is no such switch, the plan is probably a work Enterprise seat and the Owner has to do it.
2. Start a brand-new session in the Apollo Project and ask Claude to list its tools. If there is no `Claude_Docs` entry, the switch works.
3. If the tools are still there, check the thread's + > Connectors list at claude.ai/code for a Docs entry and switch it off there, since that choice becomes the account default. If Docs is not in that list, report it through Help > Send feedback and quote issue #509.

---

## Sources actually used

- https://support.claude.com/en/articles/16923645-get-started-with-claude-docs
- https://support.claude.com/en/articles/9487310-what-are-artifacts-and-how-do-i-use-them
- https://support.claude.com/en/articles/14604406-claude-design-admin-guide-for-team-and-enterprise-plans
- https://support.claude.com/en/articles/14604416-get-started-with-claude-design
- https://support.claude.com/en/articles/16761823-claude-cowork-and-chat-are-one-claude
- https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities
- https://support.claude.com/en/articles/13730515-manage-claude-s-tool-access
- https://support.claude.com/en/articles/12138966-release-notes
- https://claude.com/blog/cowork-is-now-claude
- https://claude.com/docs/cowork/changelog
- https://claude.com/docs/connectors/custom/remote-mcp
- https://code.claude.com/docs/en/mcp
- https://code.claude.com/docs/en/claude-projects
- https://code.claude.com/docs/en/desktop
- https://github.com/anthropics/claude-ai-mcp/issues/509
- https://github.com/anthropics/claude-code/issues/82498
- https://github.com/anthropics/claude-code/issues/22301
- https://github.com/anthropics/claude-code/issues/81460
- Press, used only for dates: https://venturebeat.com/technology/anthropic-is-killing-off-cowork-and-folding-it-into-claude-launching-claude-docs-and-claude-slides · https://www.engadget.com/2259938/anthropics-claude-can-now-create-editable-documents-for-you-cowork-chat-together/ · https://thenextweb.com/news/anthropic-claude-cowork-merge-docs-slides

Limits: GitHub issue search could not be reached from the research container (403 and robots rules), so the GitHub check is limited to issues surfaced by web search. No Reddit or community thread about Claude Docs and this error was found.
