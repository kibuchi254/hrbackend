"""
AI Service Integration - Supports both Gemini and Claude AI
Provides smart features for HR, Payroll, and Recruitment
"""
import httpx
import json
import time
from typing import Optional, Dict, Any
from app.core.config import settings


class AIService:
    """Base AI Service class"""

    def __init__(self, provider: str, api_key: str, model: str):
        self.provider = provider  # 'gemini' or 'claude'
        self.api_key = api_key
        self.model = model
        self.base_url = self._get_base_url()

    def _get_base_url(self) -> str:
        """Get the base URL for the AI provider"""
        if self.provider == "gemini":
            return "https://generativelanguage.googleapis.com/v1beta"
        elif self.provider == "claude":
            return "https://api.anthropic.com/v1"
        raise ValueError(f"Unknown provider: {self.provider}")

    async def generate_job_description(
        self,
        job_title: str,
        requirements: str,
        skills: list,
        experience_level: str,
        company_name: str
    ) -> Dict[str, Any]:
        """Generate an AI-powered job description"""

        if self.provider == "gemini":
            return await self._gemini_generate_job_description(
                job_title, requirements, skills, experience_level, company_name
            )
        elif self.provider == "claude":
            return await self._claude_generate_job_description(
                job_title, requirements, skills, experience_level, company_name
            )

    async def analyze_candidate(
        self,
        resume_text: str,
        job_requirements: str,
        job_description: str
    ) -> Dict[str, Any]:
        """Analyze a candidate's resume against job requirements"""

        if self.provider == "gemini":
            return await self._gemini_analyze_candidate(
                resume_text, job_requirements, job_description
            )
        elif self.provider == "claude":
            return await self._claude_analyze_candidate(
                resume_text, job_requirements, job_description
            )

    async def generate_interview_questions(
        self,
        job_title: str,
        job_description: str,
        candidate_profile: str,
        interview_type: str = "behavioral"
    ) -> Dict[str, Any]:
        """Generate AI-powered interview questions"""

        if self.provider == "gemini":
            return await self._gemini_generate_interview_questions(
                job_title, job_description, candidate_profile, interview_type
            )
        elif self.provider == "claude":
            return await self._claude_generate_interview_questions(
                job_title, job_description, candidate_profile, interview_type
            )

    async def analyze_interview(
        self,
        interview_transcript: str,
        job_requirements: str
    ) -> Dict[str, Any]:
        """Analyze interview transcript for insights"""

        if self.provider == "gemini":
            return await self._gemini_analyze_interview(
                interview_transcript, job_requirements
            )
        elif self.provider == "claude":
            return await self._claude_analyze_interview(
                interview_transcript, job_requirements
            )

    async def generate_salary_insights(
        self,
        job_title: str,
        location: str,
        experience_level: str,
        skills: list
    ) -> Dict[str, Any]:
        """Generate AI-powered salary insights"""

        if self.provider == "gemini":
            return await self._gemini_generate_salary_insights(
                job_title, location, experience_level, skills
            )
        elif self.provider == "claude":
            return await self._claude_generate_salary_insights(
                job_title, location, experience_level, skills
            )

    async def get_performance_review_suggestions(
        self,
        employee_name: str,
        role: str,
        achievements: str,
        areas_for_improvement: str
    ) -> Dict[str, Any]:
        """Generate AI suggestions for performance reviews"""

        if self.provider == "gemini":
            return await self._gemini_performance_review(
                employee_name, role, achievements, areas_for_improvement
            )
        elif self.provider == "claude":
            return await self._claude_performance_review(
                employee_name, role, achievements, areas_for_improvement
            )

    # ========== GEMINI AI METHODS ==========

    async def _gemini_generate_job_description(
        self,
        job_title: str,
        requirements: str,
        skills: list,
        experience_level: str,
        company_name: str
    ) -> Dict[str, Any]:
        """Generate job description using Gemini AI"""

        prompt = f"""You are an expert HR professional. Create a compelling job description for the following position:

Job Title: {job_title}
Company: {company_name}
Experience Level: {experience_level}
Key Requirements: {requirements}
Required Skills: {', '.join(skills)}

Please provide:
1. A catchy job summary
2. Detailed responsibilities (5-7 bullet points)
3. Comprehensive requirements (5-7 bullet points)
4. Preferred qualifications
5. Benefits and perks
6. Why this company is a great place to work

Format the response as JSON with keys: summary, responsibilities, requirements, preferred_qualifications, benefits, why_join_us
"""

        response = await self._call_gemini_api(prompt)
        return self._parse_json_response(response)

    async def _gemini_analyze_candidate(
        self,
        resume_text: str,
        job_requirements: str,
        job_description: str
    ) -> Dict[str, Any]:
        """Analyze candidate using Gemini AI"""

        prompt = f"""You are an expert recruiter. Analyze this candidate's resume against the job requirements:

JOB REQUIREMENTS:
{job_requirements}

JOB DESCRIPTION:
{job_description}

CANDIDATE RESUME:
{resume_text[:4000]}

Provide:
1. Match score (0-5 scale)
2. Key strengths found
3. Potential gaps
4. Recommended interview questions (3-5)
5. Overall assessment (2-3 sentences)
6. List of matched keywords

Format as JSON with keys: match_score, strengths, gaps, interview_questions, assessment, matched_keywords
"""

        response = await self._call_gemini_api(prompt)
        return self._parse_json_response(response)

    async def _gemini_generate_interview_questions(
        self,
        job_title: str,
        job_description: str,
        candidate_profile: str,
        interview_type: str
    ) -> Dict[str, Any]:
        """Generate interview questions using Gemini AI"""

        prompt = f"""Generate {interview_type} interview questions for this position:

JOB TITLE: {job_title}
JOB DESCRIPTION: {job_description}

CANDIDATE PROFILE:
{candidate_profile}

Provide 8-10 tailored questions with:
1. Question text
2. What to look for in the answer
3. Rating scale (1-5)

Format as JSON with key: questions (array of objects with question, evaluation_criteria, rating_scale)
"""

        response = await self._call_gemini_api(prompt)
        return self._parse_json_response(response)

    async def _gemini_analyze_interview(
        self,
        interview_transcript: str,
        job_requirements: str
    ) -> Dict[str, Any]:
        """Analyze interview transcript using Gemini AI"""

        prompt = f"""Analyze this interview transcript:

INTERVIEW TRANSCRIPT:
{interview_transcript[:4000]}

JOB REQUIREMENTS:
{job_requirements}

Provide:
1. Candidate's strengths shown
2. Areas of concern
3. Sentiment analysis (positive/neutral/negative)
4. Overall rating (1-5)
5. Recommended next steps
6. Key insights

Format as JSON with keys: strengths, concerns, sentiment, overall_rating, next_steps, insights
"""

        response = await self._call_gemini_api(prompt)
        return self._parse_json_response(response)

    async def _gemini_generate_salary_insights(
        self,
        job_title: str,
        location: str,
        experience_level: str,
        skills: list
    ) -> Dict[str, Any]:
        """Generate salary insights using Gemini AI"""

        prompt = f"""Provide salary insights for this position:

Job Title: {job_title}
Location: {location}
Experience Level: {experience_level}
Skills: {', '.join(skills)}

Provide:
1. Recommended salary range (min, max)
2. Market comparison
3. Influencing factors
4. Negotiation tips

Format as JSON with keys: salary_min, salary_max, market_comparison, factors, negotiation_tips
"""

        response = await self._call_gemini_api(prompt)
        return self._parse_json_response(response)

    async def _gemini_performance_review(
        self,
        employee_name: str,
        role: str,
        achievements: str,
        areas_for_improvement: str
    ) -> Dict[str, Any]:
        """Generate performance review using Gemini AI"""

        prompt = f"""Write a professional performance review:

Employee: {employee_name}
Role: {role}

ACHIEVEMENTS:
{achievements}

AREAS FOR IMPROVEMENT:
{areas_for_improvement}

Provide:
1. Opening statement
2. Key accomplishments (3-5)
3. Areas for development (3-5)
4. Goals for next period (3-5)
5. Overall rating
6. Encouraging closing

Format as JSON with keys: opening, accomplishments, development_areas, goals, rating, closing
"""

        response = await self._call_gemini_api(prompt)
        return self._parse_json_response(response)

    # ========== CLAUDE AI METHODS ==========

    async def _claude_generate_job_description(
        self,
        job_title: str,
        requirements: str,
        skills: list,
        experience_level: str,
        company_name: str
    ) -> Dict[str, Any]:
        """Generate job description using Claude AI"""

        prompt = f"""You are an expert HR professional. Create a compelling job description for the following position:

Job Title: {job_title}
Company: {company_name}
Experience Level: {experience_level}
Key Requirements: {requirements}
Required Skills: {', '.join(skills)}

Please provide a comprehensive job description in JSON format with:
- summary: A catchy job summary
- responsibilities: Array of 5-7 detailed bullet points
- requirements: Array of 5-7 comprehensive requirements
- preferred_qualifications: Array of preferred skills/qualifications
- benefits: Array of benefits and perks
- why_join_us: Compelling reasons to join the company

Respond with valid JSON only.
"""

        response = await self._call_claude_api(prompt)
        return self._parse_json_response(response)

    async def _claude_analyze_candidate(
        self,
        resume_text: str,
        job_requirements: str,
        job_description: str
    ) -> Dict[str, Any]:
        """Analyze candidate using Claude AI"""

        prompt = f"""You are an expert technical recruiter. Analyze this candidate's resume:

JOB REQUIREMENTS:
{job_requirements}

JOB DESCRIPTION:
{job_description}

CANDIDATE RESUME (first 4000 chars):
{resume_text[:4000]}

Provide analysis in JSON format:
- match_score: Number from 0-5
- strengths: Array of key strengths found
- gaps: Array of potential gaps or concerns
- interview_questions: Array of 3-5 targeted interview questions
- assessment: 2-3 sentence overall assessment
- matched_keywords: Array of matched technical terms and skills

Respond with valid JSON only.
"""

        response = await self._call_claude_api(prompt)
        return self._parse_json_response(response)

    async def _claude_generate_interview_questions(
        self,
        job_title: str,
        job_description: str,
        candidate_profile: str,
        interview_type: str
    ) -> Dict[str, Any]:
        """Generate interview questions using Claude AI"""

        prompt = f"""Generate {interview_type} interview questions:

JOB TITLE: {job_title}
JOB DESCRIPTION:
{job_description}

CANDIDATE PROFILE:
{candidate_profile}

Create 8-10 tailored questions in JSON format:
- questions: Array where each question has:
  - question: The question text
  - evaluation_criteria: What to evaluate
  - rating_scale: 1-5 rating explanation

Respond with valid JSON only.
"""

        response = await self._call_claude_api(prompt)
        return self._parse_json_response(response)

    async def _claude_analyze_interview(
        self,
        interview_transcript: str,
        job_requirements: str
    ) -> Dict[str, Any]:
        """Analyze interview transcript using Claude AI"""

        prompt = f"""Analyze this interview transcript:

INTERVIEW TRANSCRIPT (first 4000 chars):
{interview_transcript[:4000]}

JOB REQUIREMENTS:
{job_requirements}

Provide analysis in JSON format:
- strengths: Array of demonstrated strengths
- concerns: Array of areas of concern
- sentiment: "positive", "neutral", or "negative"
- overall_rating: Number 1-5
- next_steps: Array of recommended next steps
- insights: Array of key insights

Respond with valid JSON only.
"""

        response = await self._call_claude_api(prompt)
        return self._parse_json_response(response)

    async def _claude_generate_salary_insights(
        self,
        job_title: str,
        location: str,
        experience_level: str,
        skills: list
    ) -> Dict[str, Any]:
        """Generate salary insights using Claude AI"""

        prompt = f"""Provide salary market insights:

Job Title: {job_title}
Location: {location}
Experience Level: {experience_level}
Skills: {', '.join(skills)}

Provide insights in JSON format:
- salary_min: Recommended minimum
- salary_max: Recommended maximum
- market_comparison: Comparison to market average
- factors: Array of influencing factors
- negotiation_tips: Array of 3-5 negotiation tips

Respond with valid JSON only.
"""

        response = await self._call_claude_api(prompt)
        return self._parse_json_response(response)

    async def _claude_performance_review(
        self,
        employee_name: str,
        role: str,
        achievements: str,
        areas_for_improvement: str
    ) -> Dict[str, Any]:
        """Generate performance review using Claude AI"""

        prompt = f"""Write a professional performance review:

Employee: {employee_name}
Role: {role}

ACHIEVEMENTS:
{achievements}

AREAS FOR IMPROVEMENT:
{areas_for_improvement}

Provide in JSON format:
- opening: Professional opening statement
- accomplishments: Array of 3-5 key accomplishments
- development_areas: Array of 3-5 areas for growth
- goals: Array of 3-5 goals for next period
- rating: Overall performance rating
- closing: Encouraging closing statement

Respond with valid JSON only.
"""

        response = await self._call_claude_api(prompt)
        return self._parse_json_response(response)

    # ========== API CALL METHODS ==========

    async def _call_gemini_api(self, prompt: str) -> str:
        """Call Gemini API"""
        url = f"{self.base_url}/models/{self.model}:generateContent"

        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{url}?key={self.api_key}",
                headers=headers,
                json=data
            )
            response.raise_for_status()

            result = response.json()
            return result["candidates"][0]["content"]["parts"][0]["text"]

    async def _call_claude_api(self, prompt: str) -> str:
        """Call Claude API"""
        url = f"{self.base_url}/messages"

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "max_tokens": 4096,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()

            result = response.json()
            return result["content"][0]["text"]

    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON response from AI"""
        try:
            # Try to find JSON in response
            start = response.find("{")
            end = response.rfind("}") + 1
            if start != -1 and end > start:
                return json.loads(response[start:end])
            return json.loads(response)
        except json.JSONDecodeError:
            # Return raw text if JSON parsing fails
            return {"raw_response": response}


def get_ai_service(company_id: int, provider: str = "gemini") -> AIService:
    """Factory function to get AI service instance"""

    # In production, fetch from database based on company_id
    # For now, use environment variables
    if provider == "gemini":
        api_key = settings.GEMINI_API_KEY if hasattr(settings, 'GEMINI_API_KEY') else ""
        model = settings.GEMINI_MODEL if hasattr(settings, 'GEMINI_MODEL') else "gemini-pro"
    else:  # claude
        api_key = settings.CLAUDE_API_KEY if hasattr(settings, 'CLAUDE_API_KEY') else ""
        model = settings.CLAUDE_MODEL if hasattr(settings, 'CLAUDE_MODEL') else "claude-3-sonnet"

    return AIService(provider=provider, api_key=api_key, model=model)
