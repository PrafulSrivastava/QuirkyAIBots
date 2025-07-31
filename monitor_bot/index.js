
import fetch from "node-fetch";

export default (app) => {
  app.log.info("Yay, the app was loaded!");
  app.onAny((context) => {
    console.log(`Received event: ${context.name}.${context.payload?.action}`);
  });

  app.on("issue_comment.created", async (context) => {
    const comment = context.payload.comment;

    if (comment.user.type === "Bot") {
      app.log.info(`Skipping bot comment by ${comment.user.login}`);
      return;
    }

    const issue = context.payload.issue;
    const repo = context.payload.repository.full_name;
    const commentText = comment.body;

    app.log.info(`New comment on issue #${issue.number} in ${repo}: "${commentText}"`);

    try {
      const response = await fetch("http://assistant:8000/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ commit: { text: commentText } }),
      });

      const data = await response.json();
      const llmResponse = data.response || "🤖 Sorry, I couldn't generate a response.";

      await context.octokit.issues.createComment(
        context.issue({
          body: llmResponse,
        })
      );
    } catch (error) {
      app.log.error("Failed to get LLM response:", error);
    }
  });
};
