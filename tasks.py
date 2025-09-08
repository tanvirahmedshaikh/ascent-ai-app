from crewai import Task

class BrandingTasks:
    # --- Strategy and Ideation Tasks (no changes) ---
    def strategy_task(self, agent, user_context, target_role, target_audience, platform, duration):
        # ... (code from previous step)
        return Task(
            description=f"""Analyze the user's comprehensive background provided below.
            Based on this, create a detailed {duration}-week content plan to help them build their personal brand as a top-tier {target_role}.
            The plan should be tailored for the {target_audience} on the {platform} platform.

            USER'S BACKGROUND AND GOALS:
            {user_context}""",
            expected_output=f"A markdown document outlining a {duration}-week content plan. Each week should have a clear theme and actionable content ideas tailored for {platform}.",
            agent=agent
        )

    def refine_strategy_task(self, agent, context, critique, user_context, target_role, target_audience, platform, duration):
        # ... (code from previous step)
        return Task(
            description=f"""You are refining a personal branding content strategy based on user feedback. It is crucial that you create a new, updated plan that is significantly different from the previous version, based on the user's critique.

            USER'S FULL CONTEXT (for reference):
            {user_context}
            
            THEIR GOALS:
            - Target Role: {target_role}
            - Target Audience: {target_audience}
            - Platform: {platform}
            - Duration: {duration} weeks

            USER'S CRITIQUE of the last version:
            {critique}

            PREVIOUS STRATEGY TO BE REFINED:
            {context}

            Your task is to regenerate the entire content plan, fully incorporating the user's feedback. Acknowledge their points and explain how the new plan addresses their concerns.""",
            expected_output="A new, improved content plan that directly addresses the user's critique and is substantially different from the previous version.",
            agent=agent
        )

    def ideation_task(self, agent, context):
        # ... (code from previous step)
        return Task(
            description=f"Using the following approved content plan, generate 3 specific and engaging post ideas.\n\nCONTENT PLAN:\n{context}",
            expected_output="A list of 3 numbered post ideas, each with a compelling hook and a structured outline.",
            agent=agent
        )
        
    def title_task(self, agent, context):
        # ... (code from previous step)
        return Task(
            description=f"Create a concise, 3-5 word title for this branding strategy session. The strategy is:\n\n{context}",
            expected_output="A single line of text containing only the 3-5 word title.",
            agent=agent
        )
        
    # --- NEW Writing and QA Tasks ---
    def writing_task(self, agent, context):
        return Task(
            description=f"""Write a full, ready-to-publish LinkedIn post based on the following content idea.
            The post must be professional, engaging, and expand on the provided hook and outline.

            CONTENT IDEA:
            {context}""",
            expected_output="The complete text for a single, polished LinkedIn post, formatted with markdown.",
            agent=agent
        )
        
    def qa_task(self, agent, context):
        return Task(
            description=f"""Review the following drafted LinkedIn post for quality, clarity, tone, and strategic alignment.
            Provide a concise, bulleted list of actionable feedback for improvement. If the post is excellent, state that it is ready to publish.

            DRAFT POST:
            {context}""",
            expected_output="A bulleted list of constructive feedback OR a simple 'This post is approved and ready to publish.' statement.",
            agent=agent
        )