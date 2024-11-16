function loaderNone() {
    const days = document.querySelectorAll('.day');
        days.forEach(day => {
            day.style.animation = 'none'; // Убираем анимацию
        });

    const buttons = document.querySelector('.home-button');
    const buttons1 = document.querySelectorAll('.next-week-button');
    buttons.style.display = 'block';
    buttons1.forEach((but) => {but.style.display = 'block'})

    //console.log(buttons);
    }

function getSchedule() {
        let URL = `${window.location}getSchedule/`;
        let data_schedule;
        fetch(URL)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json(); // Преобразуем ответ в JSON
            })
            .then(data => {
                 //console.log(data); // Обрабатываем полученные данные
                 //data_schedule = data;
                 localStorage.setItem('scheduleArray', JSON.stringify(data));
                 localStorage.setItem('currentWeek', numberWeek);
                 //console.log(numberWeek);
                 parseSchedule(data, numberWeek);
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
                window.location.replace(window.location);
           });

           }


function nextWeek() {
    data = JSON.parse(localStorage.getItem('scheduleArray'));
    weekNum = parseInt(localStorage.getItem('currentWeek'));
    localStorage.setItem('currentWeek', weekNum+1);
    //console.log(data)
    parseSchedule(data, weekNum+1);
    //console.log(data);
    //console.log(weekNum);
}

function beforeWeek() {
    data = JSON.parse(localStorage.getItem('scheduleArray'));
    weekNum = parseInt(localStorage.getItem('currentWeek'));
    localStorage.setItem('currentWeek', weekNum-1);
    //console.log(data)
    parseSchedule(data, weekNum-1);
    //console.log(data);
    //console.log(weekNum);
}

function parseSchedule(items, weekNumIn) {
        //console.log('Ok')
        const parentElement = document.getElementById('calendar');
        parentElement.innerHTML = "";

        items['items'].forEach((el) => {

        if (el.number === weekNumIn) {
            el.days.forEach((day) => {
                dayWeekDay = day.info.dayText
                let divDay = document.createElement('div');
                divDay.className = 'day';
                divDayHeader = document.createElement('div');
                divDayHeader.className = 'day-header';
                divDayHeader.textContent = day.info.dayText;
                divDate = document.createElement('div');
                divDate.className = 'date';
                divDate.textContent = day.info.dateText;
                divDay.appendChild(divDayHeader);
                divDay.appendChild(divDate);
                parentElement.appendChild(divDay);

                //console.log(day.info);

                day.lessons.forEach((lesson) => {

                    lessonNumber = lesson.number
                    lessonTimeRange = lesson.timeRange
                    lessonName = lesson.lessonName
                    auditoryName = lesson.auditoryName
                    teacherName = lesson.teacherName
                    htmlTypeLesson = lesson.htmlTypeLesson
                    textTypeLesson = lesson.textTypeLesson
                    //typeLessonOrig = lesson.typeLessonOrig
                    //console.log(dayWeekDay, lessonNumber, lessonTimeRange, lessonName, auditoryName, teacherName, htmlTypeLesson, textTypeLesson)


                    let lessonHTML = document.createElement('div');


                    if (lesson.isDistant === true) {
                        lessonHTML.className = 'dist';
                        auditoryName = 'Дистант';

                    }
                    else {
                        lessonHTML.className = htmlTypeLesson;
                        //console.log(htmlTypeLesson)
                    }



                    lessonHTML.textContent = `${lessonTimeRange} - ${lessonName} ${textTypeLesson}`
                    eventDetails = document.createElement('div');
                    eventDetails.className = 'event-details';

                    eventDetails.textContent = `Кабинет: ${auditoryName} | Преподаватель: ${teacherName}`

                    lessonHTML.appendChild(eventDetails);

                    divDay.appendChild(lessonHTML)

                })

            })

        }


        })

    loaderNone();
    }


window.onload = function() {getSchedule()}