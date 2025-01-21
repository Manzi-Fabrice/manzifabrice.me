/********************/
/* Javascript Part: Lab 02, COSC 52*/
/********************/

function startQuiz() {
  document.getElementById("front-page").style.display = "none";
  document.querySelector("header").style.display = "block";
  document.getElementById("questions").style.display = "block";

  const allQuestions = document.querySelectorAll(".question_screen");
  allQuestions.forEach((question) => {
    question.style.display = "none";
  });
  document.getElementById("question1").style.display = "block";

  updateProgressBar();
}

function goToNext(current) {
  const currentScreen = document.getElementById(`question${current}`);
  const nextScreen = document.getElementById(`question${current + 1}`);

  if (nextScreen) {
    currentScreen.style.display = "none";
    nextScreen.style.display = "block";
  }
  updateProgressBar();
}

function goToPrevious(current) {
  const currentScreen = document.getElementById(`question${current}`);
  const previousScreen = document.getElementById(`question${current - 1}`);

  if (previousScreen) {
    currentScreen.style.display = "none";
    previousScreen.style.display = "block";
  }
  updateProgressBar();
}

function updateProgressBar() {
  const totalQuestions = 7;
  let answeredCount = 0;

  for (let i = 1; i <= totalQuestions; i++) {
    const selected = document.querySelector(`input[name="q${i}"]:checked`);
    if (selected) {
      answeredCount++;
    }
  }

  const progressPercentage = (answeredCount / totalQuestions) * 100;
  document.getElementById("progress").style.width = progressPercentage + "%";
}

function calculateScore() {
  let total = 0;
  for (let i = 1; i <= 7; i++) {
    const selected = document.querySelector(`input[name="q${i}"]:checked`);

    if (selected) {
      total += parseInt(selected.getAttribute("data-score"));
    }
  }
  return total;
}

function allQuestionsAnswered() {
  for (let i = 1; i <= 7; i++) {
    const selected = document.querySelector(`input[name="q${i}"]:checked`);
    if (!selected) {
      return false;
    }
  }
  return true;
}

function showResults() {
  const resultSection = document.getElementById("Results");
  const quizSection = document.getElementById("questions");
  const resultTitle = document.getElementById("ResultClass");
  const resultDescription = document.getElementById("ResultDescription");

  if (!allQuestionsAnswered()) {
    alert("Please answer all questions before viewing results");
    return;
  }
  updateProgressBar();

  const totalScore = calculateScore();

  if (totalScore >= 15) {
    resultTitle.innerText = "CS52 Mastermind";
    resultDescription.innerText =
      "You’ve got what it takes to survive and thrive in CS52! Debugging and styling are no match for your skills. Keep crushing it!";
  } else if (totalScore >= 10) {
    resultTitle.innerText = "CS52 Survivor";
    resultDescription.innerText =
      "It’s tough, but you’ve got the grit to pull through. Just don’t forget to ask for help when you need it!";
  } else if (totalScore >= 6) {
    resultTitle.innerText = "CS52 Struggler (but with Style)";
    resultDescription.innerText =
      "You’re keeping up… kind of. The struggle is real, but so is your determination. You’ll make it—eventually!";
  } else {
    resultTitle.innerText = "CS52 Dropout (Emotionally)";
    resultDescription.innerText =
      "You’re mentally done, but hey, you showed up. Maybe next time, JavaScript will be kinder to you.";
  }

  quizSection.style.display = "none";
  resultSection.style.display = "block";
}

function Home() {
  document.getElementById("front-page").style.display = "block";
  document.querySelector("header").style.display = "none";
  document.getElementById("Results").style.display = "none";

  const allQuestions = document.querySelectorAll(".question_screen");
  allQuestions.forEach((question) => {
    question.style.display = "none";
  });

  document.querySelectorAll('input[type="radio"]:checked').forEach((radio) => {
    radio.checked = false;
  });
  document.getElementById("progress").style.width = "0%";
}
