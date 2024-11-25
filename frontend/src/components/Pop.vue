<template>
    <div v-if="showPopup" class="popup">
        <div class="popup-content">

            <div v-if="!showStudyMaterial && !showQuestions && !showCloseButton" class="alert-popup">

            <h1 class="blinking">You Have Been Phished!</h1>
                <img src="\RIA_logo.jpeg" alt="Company Logo" class="ria-logo">
                <div class="warning-text">
                    <p>This was a Phishing Simulation exercise conducted by RIA Advisory under the guidance of RIA CISO Salman Ansari. You shouldn't have clicked on the link. You can see that this email was generated from outside. The email is from a different domain than RIA Advisory. You should be cautious before clicking any unknown link that is from outside and enticing you to click on some link.</p>
                </div>
                <p class="warning">As you clicked on the link, it is mandatory for you to complete the RIA Phishing training. RIA InfoSec team will schedule the phishing awareness training session and Quiz for you shortly.</p>
                <button class="button-primary" @click="closePopup">
                        Close
                    </button>
            </div>
        </div>
    </div>
</template>

<script>
export default {

    props: {
       colleague_id: {
           type: String,
           required: true,
       },
   },

   
    data() {
        return {
            showPopup: false,
            showStudyMaterial: false,
            showQuestions: false,
            showCloseButton: false,
            colleague_id: null,
        };
    },
    created() {
        const colleagueId = this.$route.params.colleague_id;
        this.fetchData(colleagueId);

        if (this.$route.path.startsWith('/study-material')) {
            this.showStudyMaterial = true;
            this.trackPresentationCompletion();
        }
    },

    mounted() {
        this.colleague_id = this.$route.params.colleague_id;
    },

    methods: {

        async fetchData(colleagueId) {
            console.log('Fetching data for colleague ID:', colleagueId);
            try {
                const response = await fetch(`https://trial-ria-app.onrender.com/phishing_opened/${colleagueId}`);
                // const response = await fetch(`http://127.0.0.1:5000/phishing_opened/${colleagueId}`);
                const data = await response.json();
                console.log('Response data:', data);
                if (data.showPopup) {
                    this.showPopup = true;
                } else {
                    this.showPopup = false;
                }
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        },

        closePopup() {
            this.showPopup = false;
            window.close();
        },
    }
};
</script>

<style scoped>

.popup {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.9);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 20px;
}

.popup-content {
    background: #ffffff;
    border-radius: 16px;
    width: 100%;
    max-width: 800px;
    max-height: 90vh;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    padding: 20px;
    text-align: center;
    overflow-y: auto;
    animation: fadeIn 0.3s ease-in-out;
}

.button-primary {
    padding: 10px 15px;
    font-size: 1.1em;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin-top: 20px;
}

.button-primary {
    background-color: #007bff;
    color: white;
    transition: background 0.2s;
}

.button-primary:hover {
    background-color: #0056b3;
}

.button-primary {
    padding: 10px 15px;
    font-size: 1.1em;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin-top: 20px;
    background-color: #007bff;
    color: white;
    transition: background 0.2s;
}

.button-primary:disabled {
    background-color: #ccc;
    color: #666;
    cursor: not-allowed;
}

.button-primary:not(:disabled):hover {
    background-color: #0056b3;
}

.alert-popup {
    background-color: #fff3cd;
    border: 1px solid #ffeeba;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    max-width: 600px;
    margin: 20px auto;
    text-align: center;
}

.warning-text {
    color: #856404;
    font-size: 16px;
    line-height: 1.5;
    margin-bottom: 10px;
}

.blinking {
    animation: blink-animation 1s steps(5, start) infinite;
}

@keyframes blink-animation {
    to {
        visibility: hidden;
    }
}

h1 {
    color: #dc3545;
    text-align: center;
}

p {
    margin-bottom: 15px;
}

.warning {
   background-color: #ffeeba;
    border-left: 6px solid #ffc107;
    padding: 10px;
    margin: 20px 0;
}

.ria-logo {
    width: 100px;
    height: auto;
}
</style>



