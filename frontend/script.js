document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('upload-form');
    const loadingDiv = document.getElementById('loading');
    const resultDiv = document.getElementById('result');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Show loading, hide result
        loadingDiv.classList.remove('d-none');
        resultDiv.classList.add('d-none');
        
        const formData = new FormData(form);

        try {
            const response = await fetch('http://localhost:5000/analyze', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Server response was not ok');
            }

            displayResults(data);
        } catch (error) {
            console.error('Error:', error);
            alert(`Error analyzing resume: ${error.message}`);
        } finally {
            loadingDiv.classList.add('d-none');
        }
    });

    function displayResults(result) {
        // Show result div
        resultDiv.classList.remove('d-none');

        // Update score
        const progressBar = document.querySelector('.progress-bar');
        const scoreText = document.querySelector('.score-text');
        progressBar.style.width = `${result.score}%`;
        scoreText.textContent = `${result.score}%`;

        // Update ATS score
        const atsProgressBar = document.querySelector('.ats-progress');
        const atsScoreText = document.querySelector('.ats-score-text');
        atsProgressBar.style.width = `${result.ats_score}%`;
        atsScoreText.textContent = `${result.ats_score}%`;
        
        // Display ATS metrics
        const atsMetricsDiv = document.getElementById('ats-metrics');
        if (atsMetricsDiv && result.ats_details) {
            atsMetricsDiv.innerHTML = Object.entries(result.ats_details)
                .map(([metric, score]) => `
                    <div class="ats-metric">
                        <div class="metric-label">${formatMetricName(metric)}</div>
                        <div class="metric-score">
                            <div class="progress">
                                <div class="progress-bar ${getScoreClass(score)}" 
                                     style="width: ${score}%"></div>
                            </div>
                            <span>${score}%</span>
                        </div>
                    </div>
                `).join('');
        }
        
        // Add ATS recommendations to suggestions
        if (result.ats_recommendations) {
            const suggestionsDiv = document.getElementById('suggestions-list');
            result.ats_recommendations.forEach(rec => {
                suggestionsDiv.innerHTML += `
                    <li class="suggestion-item ats-suggestion">
                        <i class="fas fa-robot"></i>
                        <span>${rec.message}</span>
                    </li>
                `;
            });
        }

        // Update sections check
        const sectionsDiv = document.getElementById('sections-list');
        if (sectionsDiv) {
            sectionsDiv.innerHTML = '';
            for (const [section, found] of Object.entries(result.sections_found)) {
                const icon = found ? 'check-circle' : 'times-circle';
                const status = found ? 'found' : 'missing';
                sectionsDiv.innerHTML += `
                    <div class="section-check">
                        <i class="fas fa-${icon} ${status}"></i>
                        <span class="text-capitalize">${section}</span>
                    </div>
                `;
            }
        }

        // Update skills and keywords
        const technicalList = document.getElementById('technical-skills-list');
        const toolsList = document.getElementById('tools-list');
        const softSkillsList = document.getElementById('soft-skills-list');
        const statsDiv = document.getElementById('skills-stats');

        if (result.keywords) {
            const categorizedSkills = {
                technical: [],
                tools: [],
                soft: []
            };

            // Categorize skills
            Object.entries(result.keywords).forEach(([keyword, info]) => {
                const skillData = {
                    name: keyword,
                    count: info.count || 1,
                    confidence: info.confidence || 'Medium'
                };

                if (isSoftSkill(keyword)) {
                    categorizedSkills.soft.push(skillData);
                } else if (isToolOrFramework(keyword)) {
                    categorizedSkills.tools.push(skillData);
                } else {
                    categorizedSkills.technical.push(skillData);
                }
            });

            // Display skills by category
            if (technicalList) {
                technicalList.innerHTML = renderSkillBadges(categorizedSkills.technical);
            }
            if (toolsList) {
                toolsList.innerHTML = renderSkillBadges(categorizedSkills.tools);
            }
            if (softSkillsList) {
                softSkillsList.innerHTML = renderSkillBadges(categorizedSkills.soft);
            }

            // Update statistics
            if (statsDiv) {
                statsDiv.innerHTML = `
                    <div class="stats-grid">
                        <div class="stat-item">
                            <div class="stat-value">${Object.keys(result.keywords).length}</div>
                            <div class="stat-label">Total Skills</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">${categorizedSkills.technical.length}</div>
                            <div class="stat-label">Technical Skills</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">${categorizedSkills.tools.length}</div>
                            <div class="stat-label">Tools & Technologies</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">${categorizedSkills.soft.length}</div>
                            <div class="stat-label">Soft Skills</div>
                        </div>
                    </div>
                `;
            }
        }

        // Continue with suggestions and roles display
        displaySuggestions(result.suggestions);
        displayRoles(result.suitable_roles);

        // Update roles list
        const rolesDiv = document.getElementById('roles-list');
        if (rolesDiv && result.suitable_roles) {
            rolesDiv.innerHTML = result.suitable_roles.map(role => `
                <div class="role-card">
                    <div class="role-icon">
                        <i class="fas ${getRoleIcon(role.role)}"></i>
                    </div>
                    <div class="role-details">
                        <div class="role-match">
                            <h6 class="mb-0">${formatRoleTitle(role.role)}</h6>
                            <span class="match-score">${role.confidence.toFixed(0)}% Match</span>
                        </div>
                        <div class="role-skills">
                            ${role.matched_keywords.slice(0, 5).map(skill => `
                                <span class="role-skill-badge">${skill}</span>
                            `).join('')}
                        </div>
                    </div>
                </div>
            `).join('');
        }
    }

    function displaySuggestions(suggestions) {
        const suggestionsUl = document.getElementById('suggestions-list');
        suggestionsUl.innerHTML = '';
        
        suggestions.forEach(suggestion => {
            const li = document.createElement('li');
            li.className = `suggestion-item ${suggestion.type}-suggestion`;
            
            li.innerHTML = `
                <div class="suggestion-header">
                    <span class="suggestion-icon">${suggestion.icon}</span>
                    <span class="suggestion-title">${suggestion.title}</span>
                </div>
                <div class="suggestion-message">
                    ${suggestion.message}
                </div>
            `;
            
            suggestionsUl.appendChild(li);
        });
    }

    function displayRoles(roles) {
        const rolesDiv = document.getElementById('roles-list');
        rolesDiv.innerHTML = roles.map(role => `
            <div class="role-card ${getMatchClass(role.confidence)}">
                <div class="role-header">
                    <div class="role-title-section">
                        <i class="fas ${getRoleIcon(role.role)}"></i>
                        <h5 class="role-title">${formatRoleTitle(role.role)}</h5>
                    </div>
                    <div class="confidence-score">
                        <div class="score-circle">
                            <span class="score-value">${role.confidence.toFixed(1)}%</span>
                            <span class="score-label">Match</span>
                        </div>
                    </div>
                </div>
                
                <div class="role-content">
                    <div class="matched-skills">
                        <h6>Matched Skills</h6>
                        <div class="skills-list">
                            ${role.matched_keywords.map(skill => 
                                `<span class="skill-match">${skill}</span>`
                            ).join('')}
                        </div>
                    </div>
                    
                    <div class="missing-skills">
                        <h6>Required Skills</h6>
                        <div class="skills-list">
                            ${getMissingSkills(role.requirements, role.matched_keywords).map(skill =>
                                `<span class="skill-missing">${skill}</span>`
                            ).join('')}
                        </div>
                    </div>
                </div>
            </div>
        `).join('');
    }

    function getMatchClass(confidence) {
        if (confidence >= 80) return 'excellent-match';
        if (confidence >= 60) return 'good-match';
        if (confidence >= 40) return 'fair-match';
        return 'poor-match';
    }

    function getRoleIcon(role) {
        const icons = {
            'software_engineer': 'fa-code',
            'data_scientist': 'fa-chart-line',
            'web_developer': 'fa-globe',
            'devops_engineer': 'fa-server',
            'mobile_developer': 'fa-mobile-alt',
            'ui_ux_designer': 'fa-paint-brush',
            'data_engineer': 'fa-database',
            'cloud_architect': 'fa-cloud',
            'security_engineer': 'fa-shield-alt',
            'ml_engineer': 'fa-brain'
        };
        return icons[role] || 'fa-laptop-code';
    }

    function formatRoleTitle(role) {
        return role.split('_')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }

    function getMissingSkills(requirements, matched) {
        const matchedSet = new Set(matched.map(s => s.toLowerCase()));
        return requirements.filter(skill => !matchedSet.has(skill.toLowerCase()));
    }

    // Helper functions
    function renderSkillBadges(skills) {
        return skills.map(skill => `
            <div class="skill-badge">
                <span class="skill-level ${getConfidenceClass(skill.confidence)}" 
                      title="${skill.confidence} confidence"></span>
                ${skill.name}
                ${skill.count > 1 ? `<span class="count">${skill.count}</span>` : ''}
            </div>
        `).join('');
    }

    function getConfidenceClass(confidence) {
        const levels = {
            'High': 'expert',
            'Medium': 'advanced',
            'Low': 'intermediate'
        };
        return levels[confidence] || 'beginner';
    }

    // Helper functions for skill categorization
    function isToolOrFramework(keyword) {
        const toolPatterns = [
            'database', 'framework', 'library', 'git', 'docker', 'kubernetes',
            'aws', 'azure', 'jenkins', 'jira', 'webpack', 'npm', 'maven',
            'ide', 'editor', 'platform', 'tool', 'version control'
        ];
        return toolPatterns.some(pattern => 
            keyword.toLowerCase().includes(pattern) || 
            pattern.includes(keyword.toLowerCase())
        );
    }

    function isSoftSkill(keyword) {
        const softSkillPatterns = [
            'communication', 'leadership', 'teamwork', 'management',
            'problem solving', 'analytical', 'creativity', 'interpersonal',
            'organization', 'time management', 'adaptability', 'flexibility',
            'critical thinking', 'collaboration', 'presentation', 'negotiation',
            'conflict resolution', 'decision making', 'emotional intelligence',
            'project management', 'mentoring', 'coaching', 'soft skills'
        ];
        return softSkillPatterns.some(pattern => 
            keyword.toLowerCase().includes(pattern) || 
            pattern.includes(keyword.toLowerCase())
        );
    }

    function formatMetricName(metric) {
        return metric.split('_')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }

    function getScoreClass(score) {
        if (score >= 80) return 'bg-success';
        if (score >= 60) return 'bg-info';
        if (score >= 40) return 'bg-warning';
        return 'bg-danger';
    }
});
