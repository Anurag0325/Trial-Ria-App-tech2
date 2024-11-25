<template>
    <div>
        <nav class="navbar">
            <div class="navbar-brand">
                <img src="Xploit2Secure.jpeg" alt="Logo" class="logo" />
                <div class="navbar-buttons">
                    <button @click="logout">Logout</button>
                </div>
            </div>
        </nav>

        <div>
            <h2 class="candidate">Dashboard</h2>

            <button @click="sendPhishingEmails">Send Phishing Email</button>
            <button @click="downloadReport">Clicked Candidates Report</button>
            <button @click="emailedCandidatesReport">Emailed Candidates</button>       

            <h2 class="candidate">Candidate Reports</h2>

            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Colleague Name</th>
                        <th>Department</th>
                        <th>Link Clicked</th>
                        <th>Link Clicked Date</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="report in reports" :key="report.id">
                        <td>{{ report.id }}</td>
                        <td>{{ getColleagueName(report.colleague_id) }}</td>
                        <td>{{ getColleagueDepartment(report.colleague_id) }}</td>
                        <td>{{ report.clicked ? 'Yes' : 'No' }}</td>
                        <td>{{ formatDate(report.clicked_date) }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>


<script>

export default {
    data() {
        return {
            reports: [],
            questions: [],
            colleagues: [],
            pollingInterval: null,
            isGenerating: false,
            file: null,
            showQuestionModal: false,
            selectedDepartment: '',
            isEditing: false,
            status: "Pending",
            question: {
                id: null,
                question_text: '',
                options: ['', ''],
                answer: ''
            },
        };
    },

    methods: {
    
        formatDate(dateString) {
            if (!dateString) return 'N/A';
            const date = new Date(dateString);

            const day = date.getUTCDate().toString().padStart(2, '0');
            const month = (date.getUTCMonth() + 1).toString().padStart(2, '0');
            const year = date.getUTCFullYear();
            return `${day}-${month}-${year}`;
        },

        async downloadReport() {
      try {
        const response = await fetch('https://trial-ria-app-tech2.onrender.com/generate_dashboard_clicked_report');
        // const response = await fetch('http://127.0.0.1:5000/generate_dashboard_clicked_report');
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'clicked_candidates_report.csv';
        a.click();
        window.URL.revokeObjectURL(url);
      } catch (error) {
        console.error("Error downloading the CSV report:", error);
      }
    },



        logout() {
            fetch('https://trial-ria-app.onrender.com/logout', {
            // fetch('http://127.0.0.1:5000/logout', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json',
                },
            })
            .then(response => {
                if (response.ok) {
                localStorage.removeItem('token');
                this.$router.push('/');
                }
            })
            .catch(error => {
                console.error('Logout failed:', error);
            });
        },

        async sendPhishingEmails() {

            try {
                const response = await fetch('https://trial-ria-app-tech2.onrender.com/send_email', {
                // const response = await fetch('http://127.0.0.1:5000/send_email', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const data = await response.json();
                this.message = data.message;
                alert("Email Send to Candidates")
            } catch (error) {
                console.error('Failed to send emails:', error);
                this.message = 'Error sending emails. Please try again.';
                alert("Email is Not Send to Candidates")
            }
        },

        async fetchReports() {
            try {
                const response = await fetch('https://trial-ria-app-tech2.onrender.com/get_all_reports');
            // const response = await fetch('http://127.0.0.1:5000/get_all_reports');
                if (!response.ok) {
                    throw new Error('Failed to fetch reports');
                }
                const data = await response.json();
                this.reports = data.reports;
            } catch (error) {
                console.error('Error fetching reports:', error);
            }
        },

        async fetchQuestions() {
            try {
                // const response = await fetch('https://ria-app.onrender.com/questions');
                const response = await fetch('https://trial-ria-app-tech2.onrender.com/questions');
                // const response = await fetch('http://127.0.0.1:5000/questions');
                const data = await response.json();
                this.questions = data;
            } catch (error) {
                console.error('Failed to fetch questions:', error);
            }
        },

        async fetchColleagues() {
            try {
                const response = await fetch('https://trial-ria-app-tech2.onrender.com/users');
                // const response = await fetch('http://127.0.0.1:5000/questions');
                const data = await response.json();
                this.colleagues = data;
            } catch (error) {
                console.error('Failed to fetch colleagues:', error);
            }
        },

        getColleagueName(colleagueId) {
            const colleague = this.colleagues.find(c => c.id === colleagueId);
            return colleague ? colleague.name : 'Unknown';
        },

        getColleagueDepartment(colleagueId) {
            const colleague = this.colleagues.find(c => c.id === colleagueId);
            return colleague ? colleague.department : 'Unknown';
        },

        async emailedCandidatesReport() {
            if (this.isGenerating) return;
            this.isGenerating = true;
            this.stopPolling();

            try {
                const response = await fetch(`https://trial-ria-app-tech2.onrender.com/generate_emailed_candidates_report`, {
                // const response = await fetch(`http://127.0.0.1:5000/generate_emailed_candidates_report`, {
                    method: 'GET'
                });

                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const link = document.createElement("a");
                    link.href = url;
                    link.setAttribute("download", "emailed_candidates_report.csv");
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                } else {
                    const errorData = await response.json();
                    alert(`Error: ${errorData.error || response.statusText}`);
                }
            } catch (error) {
                console.error("Error generating report:", error);
                alert("An error occurred while generating the report.");
            } finally {
                this.isGenerating = false;
                this.startPolling();
            }
        },

        startPolling() {
            this.fetchReports();
            this.pollingInterval = setInterval(async () => {
                if (!this.isGenerating) {
                    await this.fetchReports();
                }
            }, 5000);
        },

        stopPolling() {
            clearInterval(this.pollingInterval);
        },

        openQuestionModal() {
            this.showQuestionModal = true;
            this.fetchQuestions();
        },

        closeQuestionModal() {
            this.showQuestionModal = false;
            this.resetQuestionForm();
        },

        resetQuestionForm() {
            this.isEditing = false;
            this.question = {
                id: null,
                question_text: '',
                options: ['', ''],
                answer: ''
            };
        },

        async fetchQuestions() {
            try {
                const response = await fetch('https://trial-ria-app-tech2.onrender.com/questions');
                // const response = await fetch('http://127.0.0.1:5000/questions');
                const data = await response.json();
                this.questions = data;
            } catch (error) {
                console.error('Failed to fetch questions:', error);
            }
        },

        async addQuestion() {
            const response = await fetch('https://trial-ria-app-tech2.onrender.com/questions', {
            // const response = await fetch('http://127.0.0.1:5000/questions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.question)
            });
            await response.json();
            this.fetchQuestions();
            this.resetForm();
        },

        async editQuestion(question) {
            this.currentQuestionId = question.id;
            this.question = { ...question };

            if (!Array.isArray(this.question.options)) {
                this.question.options = [];
            }

            this.isEditing = true;
            this.showQuestionForm = true;
        },

        async updateQuestion() {
            if (!this.currentQuestionId) {
                alert('No question selected for updating.');
                return;
            }

            const response = await fetch(`https://trial-ria-app-tech2.onrender.com/questions/${this.currentQuestionId}`, {
            // const response = await fetch(`http://127.0.0.1:5000/${this.currentQuestionId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.question)
            });

            if (!response.ok) {
                const errorData = await response.json();
                console.error('Error updating question:', errorData);
                alert(`Error: ${errorData.error || 'Something went wrong!'}`);
                return;
            }

            const data = await response.json();
            console.log('Success:', data.message);
            this.fetchQuestions();
            this.resetForm();
        },

        async deleteQuestion(id) {
            await fetch(`https://trial-ria-app-tech2.onrender.com/questions/${id}`, {
            // await fetch(`http://127.0.0.1:5000/questions/${id}`, {
                method: 'DELETE'
            });
            this.fetchQuestions();
        },

        resetForm() {
            this.question = {
                question_text: '',
                options: ['', ''],
                answer: ''
            };
            this.isEditing = false;
            this.currentQuestionId = null;
        },

        addOption() {
            if (Array.isArray(this.question.options)) {
                if (this.question.options.length < 4) {
                    this.question.options.push('');
                } else {
                    alert('You can only add up to 4 options.');
                }
            } else {
                console.error("Options is not defined or is not an array");
            }
        },

        deleteOption(index) {
            if (this.question.options.length > 2) {
                this.question.options.splice(index, 1);
            } else {
                alert('You must have at least 2 options.');
            }
        },

        cancel() {
            this.resetQuestionForm();
        },
    },

    async mounted() {
        await this.fetchReports();
        await this.fetchQuestions();
        await this.fetchColleagues();
        this.startPolling();
    },

    beforeDestroy() {
        this.stopPolling();
    },
};
</script>


<style scoped>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Arial', sans-serif;
    background-image: linear-gradient(to right, #f0f9ff, #cbebff);
    color: #333;
    padding-top: 80px;
}


.logo {
    height: 40px;
    margin-right: 1rem;
    filter: drop-shadow(2px 2px 3px rgba(0, 0, 0, 0.2));
}

.nav-links li {
    margin-left: 20px;
}

.navbar {
    background-color: #26c8bb;
    color: white;
    padding: 1rem;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
}

.nav-links a {
    color: white;
    text-decoration: none;
    font-size: 18px;
    transition: color 0.3s ease, font-weight 0.3s ease;
}

.nav-links a:hover {
    color: #c2e8a7;
    font-weight: bold;
}

.main-content {
    margin-top: 20px;
    padding: 40px;
    background-color: #fff;
    border-radius: 12px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
    background-repeat: no-repeat;
    background-size: cover;
}

h2 {
    font-size: 28px;
    color: #444;
    border-bottom: 2px solid #69b820;
    padding-bottom: 15px;
    margin-bottom: 30px;
}

button {
    padding: 8px 10px;
    font-size: 14px;
    background-image: linear-gradient(to right, #4df19f, #34d399);
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background 0.3s ease;
    margin: 10px 20px;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15);
}

button:hover {
    background-image: linear-gradient(to right, #57a015, #4ca852);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

table {
    width: 100%;
    border-collapse: collapse;
    background-color: #f8fafc;
}

table th,
table td {
    padding: 12px;
    text-align: left;
    font-size: 14px;
    border: 1px solid #ddd;
}

table th {
    background-color: #c2e8a7;
    font-weight: bold;
}

tbody tr:nth-child(even) {
    background-color: #f1f1f1;
}

tbody tr:hover {
    background-color: #e1f5fe;
    transition: background 0.3s ease;
}


@media (max-width: 768px) {
    .main-content {
        width: 95%;
        padding: 20px;
    }

    table,
    th,
    td {
        font-size: 14px;
        padding: 10px;
    }

    button {
        padding: 10px 20px;
        font-size: 16px;
    }
}

.admin-panel {
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    margin: 1rem 0;
}

h1 {
    font-size: 24px;
    margin-bottom: 20px;
}

label {
    margin-right: 10px;
}

select {
    padding: 5px;
    margin-bottom: 20px;
}

.message {
    margin-top: 20px;
    color: green;
}

.upload-section {
    margin: 1rem 0;
}


.navbar {
    background-color: #26c8bb;
    color: white;
    padding: 1rem;
    position: relative;
    z-index: 100;
}

.navbar-brand {
    display: flex;
    align-items: center;
}


.modal-content {
    background: white;
    padding: 8px 16px;
    border-radius: 5px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    width: 800px;
    max-height: 80vh;
    display: flex;
    flex-direction: column;
}

.modal {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #fff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    z-index: 1200;
    width: 800px;
    border: 1px solid #26c8bb;
}

.questions-list {
    max-height: 300px;
    overflow-y: auto;
    margin-top: 20px;
}


.navbar-buttons {
    margin-left: auto;
}

.navbar-buttons button {
    margin-left: auto;
    background-color: #9de764;
}

.navbar-buttons button:hover {
    margin-left: auto;
    background-color: #529af3;
}

.close-button {
    padding: 6px 12px;
    font-size: 12px;
    border-radius: 4px;
    background-image: linear-gradient(to right, #f64f4f, #e53935);
    color: white;
    background-color: #f44336;
}

.modal-content h3 {
    font-size: 22px;
    margin-bottom: 15px;
}

.modal-content form {
    display: flex;
    flex-direction: column;
}

.modal-content input[type="text"],
.modal-content select {
    padding: 10px;
    font-size: 14px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    width: 100%;
}

.modal-content input::placeholder {
    color: #999;
}

.modal-content button {
    padding: 10px 20px;
    font-size: 14px;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    margin-top: 10px;
}

.modal-content button::before {
    content: "✓ ";
}

.modal-content button:hover {
    background-image: linear-gradient(to right, #f44336, #d32f2f);
}

.modal-content .close-button {
    background-color: #f44336;
}

.modal-content .close-button:hover {
    background-color: #d32f2f;
}

.modal-content button[type="button"] {
    font-size: 12px;
    padding: 8px;
    background-color: #28a745;
    margin-top: 5px;
}

.modal-content button[type="button"]:hover {
    background-color: #218838;
}

.modal-content input[type="text"] {
    font-size: 14px;
    padding: 8px;
}

.modal-content input::placeholder {
    font-size: 12px;
    color: #888;
}

.questions-list table {
    width: 100%;
    margin-top: 20px;
    border-collapse: collapse;
}

.questions-list th,
.questions-list td {
    padding: 10px;
    border: 1px solid #ddd;
}

.questions-list th {
    background-color: #f4f4f4;
    font-size: 14px;
}

.questions-list td {
    font-size: 13px;
}

.questions-list button {
    padding: 8px 12px;
    font-size: 12px;
    background-color: #0f78c8;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.questions-list h3 {
    margin-top: 1px;
    margin-bottom: 5px;
}

.questions-list button:hover {
    background-color: #57a015;
}

.options-container {
    display: flex;
    flex-direction: column;
    margin-bottom: 1rem;
}

.option-item {
    display: flex;
    align-items: center;
    margin-bottom: 0.5rem;
}

.option-item input {
    margin-right: 0.5rem;
}

.form-group {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
    position: relative;
}

.form-group select {
    padding: 10px;
    font-size: 16px;
    border-radius: 8px;
    border: 1px solid #ddd;
    width: 200px;
    appearance: none;
    background-color: #f1f1f1;
    color: #333;
    cursor: pointer;
    transition: border-color 0.3s ease;
    background-repeat: no-repeat;
    background-position: right 10px center;
}

.form-group select:hover {
    border-color: #26c8bb;
}

.form-group select:focus {
    outline: none;
    border-color: #69b820;
    box-shadow: 0 0 5px rgba(105, 184, 32, 0.5);
}

.select-label {
    font-weight: bold;
    font-size: 18px;
    margin-right: 12px;
    color: #4d4d4d;
}

.form-buttons {
    display: flex;
    gap: 10px;
}

.form-buttons button {
    padding: 10px 15px;
    font-size: 16px;
    margin-left: 5px;
    cursor: pointer;
    border: none;
    border-radius: 5px;
}

.form-buttons button:hover {
    background-color: #045b31;
    color: white;
}

.form-buttons button[type="submit"]:hover {
    background-color: #218838;
}

.form-buttons button[type="submit"] {
    background-color: #007BFF;
    color: white;
}

.form-buttons button[type="button"] {
    background-color: #dc3545;
    color: white;
}

.select-department-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    width: 100%;
    margin-bottom: 10px;
}

.select-department-label {
    font-weight: bold;
    color: #333;
    margin-bottom: 8px;
    text-align: center;
}

.select-department {
    appearance: none;
    padding: 12px 16px;
    font-size: 16px;
    border: 2px solid #26c8bb;
    border-radius: 8px;
    background-color: #f7f7f7;
    color: #333;
    position: relative;
    cursor: pointer;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
    width: 100%;
    max-width: 300px;
}

.select-department:focus,
.select-department:hover {
    border-color: #4df19f;
    background-color: #e3f7f3;
    box-shadow: 0 0 8px rgba(38, 200, 187, 0.3);
    outline: none;
}
.select-department::after {
    content: "▼";
    font-size: 12px;
    color: #666;
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
}
.select-department option {
    padding: 10px;
    background-color: #ffffff;
    color: #333;
    transition: background-color 0.2s ease;
}

.select-department option:hover {
    background-color: #26c8bb;
    color: #fff;
}

.candidate {
    padding: 10px;
}

.sending-reminder-button {
    background-color: #007bff;
    color: #fff;
    border: none;
    padding: 10px 10px;
    border-radius: 5px;
    cursor: pointer;
}

.sending-reminder-button:hover {
    background-color: #0056b3;
}

.pending-status {
    color: rgb(232, 15, 15);
    font-weight: bold;
}

</style>