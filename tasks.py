from crewai import Task
import re

class BrandingTasks:
    def summarize_resume_task(self, agent, context):
        return Task(
            description=f"""Summarize the provided resume or professional background. Identify the user's key skills, years of experience, primary industry, and infer their likely career goals.

            Frame the summary in a reflective, second-person tone. For example: 'I see you've worked in X for Y years... It looks like you're aiming for Z.'

            IMPORTANT: End your summary with the following two questions exactly as written:
            'Did I get that right? Is there anything else you would like to add that the resume doesn't cover such as things you're interested in, your hobbies, or specific aspirations?'

            USER'S BACKGROUND:
            {context}""",
            expected_output="A short, insightful summary ending with the two specific follow-up questions.",
            agent=agent
        )

    # NEW: Task to create a more detailed, intermediate content outline
    def intermediate_outline_task(self, agent, user_context, target_role, target_audience, platform, duration, positioning):
        return Task(
            description=f"""Analyze the user's comprehensive background and goals.
            Create an extremely concise, intermediate-level outline for a {duration}-week content plan to help them build their personal brand as a top-tier {target_role}.
            The outline should be tailored for the {target_audience} on the {platform} platform and reflect the user's desired positioning: '{positioning}'.
            The outline MUST be **exactly** {duration} week(s) long.
            The output should provide a weekly theme and 2-3 supporting bullet points that elaborate on the week's focus.

            Each week's entry must contain:
            1. A bolded title for the week's theme (e.g., **Week 1: Foundations & Expertise**).
            2. Exactly 2-3 brief bullet points detailing the key content areas for the week.

            DO NOT add any conversational text, introductory sentences, or additional prose. Only provide the outline.

            Example Format:
            **Week 1: Foundations & Expertise**
            - Focus on establishing foundational credibility in your field.
            - Showcase quantifiable achievements and career trajectory.
            - Share your unique perspective on industry challenges.

            USER'S BACKGROUND AND GOALS:
            {user_context}
            """,
            expected_output=f"A structured, week-by-week outline with a bolded theme and 2-3 bullet points for each of the {duration} weeks.",
            agent=agent
        )

    def strategy_task(self, agent, user_context, target_role, target_audience, platform, duration, positioning, writing_samples=""):
        return Task(
            description=f"""Analyze the user's comprehensive background and writing samples provided below.
            Based on this, create a detailed {duration}-week content plan to help them build their personal brand as a top-tier {target_role}.

            The plan MUST be **exactly** {duration} week(s) long.
            
            The plan should be tailored for the {target_audience} on the {platform} platform.
            The user's desired positioning or tone is: '{positioning}'. Ensure the content ideas and voice reflect this.

            The plan must be structured with clear daily themes. For example:
            - Monday: The "Provocative Question" Post
            - Tuesday: The "Data-Driven Insight" Post
            - Thursday: The "Case Study Snippet" Post

            USER'S BACKGROUND AND GOALS:
            {user_context}

            USER'S WRITING SAMPLES (for voice analysis):
            {writing_samples}
            """,
            expected_output=f"A markdown document outlining an **EXACTLY** {duration}-week content plan. Each week should have clear, actionable daily themes tailored for {platform} and the user's desired positioning.",
            agent=agent,
            max_retries=3,  # Add this line to retry up to 3 times
            retry_delay=5   # Add a delay of 5 seconds between retries
        )

    def refine_strategy_task(self, agent, context, critique, user_context, target_role, target_audience, platform, duration, positioning, writing_samples=""):
        return Task(
            description=f"""You are refining a personal branding content strategy based on user feedback. It is crucial that you create a new, updated plan that is significantly different from the previous version, based on the user's critique.

            USER'S FULL CONTEXT (for reference):
            {user_context}
            {writing_samples}

            THEIR GOALS:
            - Target Role: {target_role}
            - Target Audience: {target_audience}
            - Platform: {platform}
            - Duration: {duration} weeks
            - Desired Positioning: {positioning}

            USER'S CRITIQUE of the last version:
            {critique}

            PREVIOUS STRATEGY TO BE REFINED:
            {context}

            Your task is to regenerate the entire content plan, fully incorporating the user's feedback. Acknowledge their points and explain how the new plan addresses their concerns.""",
            expected_output="A new, improved content plan that directly addresses the user's critique and is substantially different from the previous version.",
            agent=agent
        )

    def ideation_task(self, agent, context):
        # Find all daily themes in the content plan using regex
        themes = re.findall(r'^-\s*(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday):\s*(.*)', context, re.MULTILINE)
        
        return Task(
            description=f"""Based on the content strategy provided, generate 2-3 concise, one-liner post ideas for EACH of the following daily themes: {', '.join(themes)}.

            The output must be structured exactly as follows, with each idea on a new line:
            
            THEME: [Name of the First Theme]
            - [Idea 1]
            - [Idea 2]
            
            THEME: [Name of the Second Theme]
            - [Idea 1]
            - [Idea 2]
            - [Idea 3]

            CONTENT STRATEGY:
            {context}
            """,
            expected_output="A structured list of one-liner post ideas grouped by their daily theme.",
            agent=agent
        )

    def refine_ideation_task(self, agent, context, critique):
        return Task(
            description=f"""A user has provided feedback on a set of LinkedIn post ideas. Your task is to generate a completely new set of ideas based on their critique.

            The new ideas should be one-liners, grouped by the original themes from the content strategy.

            USER'S CRITIQUE:
            {critique}

            REFERENCE CONTENT STRATEGY:
            {context}

            The output must be structured exactly as follows, with each idea on a new line:
            
            THEME: [Name of the First Theme]
            - [Idea 1]
            - [Idea 2]
            
            THEME: [Name of the Second Theme]
            - [Idea 1]
            - [Idea 2]
            - [Idea 3]
            """,
            expected_output="A completely new, structured list of one-liner post ideas based on user feedback.",
            agent=agent
        )

    def regenerate_ideas_task(self, agent, context, themes_to_regenerate):
        return Task(
            description=f"""Based on the provided content strategy, generate 2-3 new, concise, one-liner post ideas ONLY for the following themes: {', '.join(themes_to_regenerate)}.

            The output must be structured exactly as follows, with each idea on a new line:
            
            THEME: [Name of the First Theme to Regenerate]
            - [New Idea 1]
            - [New Idea 2]
            
            THEME: [Name of the Second Theme to Regenerate]
            - [New Idea 1]
            - [New Idea 2]
            - [New Idea 3]

            FULL CONTENT STRATEGY (for context):
            {context}
            """,
            expected_output="A structured list of new one-liner post ideas, only for the specified themes.",
            agent=agent
        )


    def title_task(self, agent, context):
        return Task(
            description=f"Create a concise, 3-5 word title for this branding strategy session. The strategy is:\n\n{context}",
            expected_output="A single line of text containing only the 3-5 word title.",
            agent=agent
        )

    def writing_task(self, agent, context):
        return Task(
            description=f"""Write a full, ready-to-publish LinkedIn post based on the following content idea.
            The post must be professional, engaging, and expand on the provided one-liner idea.

            CONTENT IDEA:
            {context}""",
            expected_output="The complete text for a single, polished LinkedIn post, formatted with markdown.",
            agent=agent
        )

    def qa_critique_task(self, agent, context):
        return Task(
            description=f"""Review the following drafted LinkedIn post for quality, clarity, tone, and strategic alignment.
            Provide a concise, bulleted list of actionable feedback for improvement. If the post is excellent, state that it is ready to publish.

            DRAFT POST:
            {context}""",
            expected_output="A bulleted list of constructive feedback OR a simple 'This post is approved and ready to publish.' statement.",
            agent=agent
        )

    def refine_writing_task(self, agent, draft, user_critique):
        return Task(
            description=f"""Refine the following draft of a LinkedIn post based on the user's feedback. Create a new, improved version that directly addresses their points.

            USER FEEDBACK:
            {user_critique}

            DRAFT TO REFINE:
            {draft}""",
            expected_output="A new, improved version of the LinkedIn post that incorporates the user's feedback.",
            agent=agent
        )