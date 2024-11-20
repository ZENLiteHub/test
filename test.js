(() => {
    let resultsAll = [];
    let leagueName = '';
    document.querySelectorAll('.history-container .eventBlock .collapsed').forEach(pn => {
        let togglePanel = (element) => {
            if (element.classList.contains('collapsed')) 
                element.childNodes[0].click();
        };
        togglePanel(pn.childNodes[0]);
    });
    document.querySelectorAll('.history-container .eventBlock').forEach(pn => {
        let weekNumber = pn.querySelector('.history__event-day')?.textContent.trim();
        let eventTime = pn.querySelector('.history__event-time')?.textContent.trim();

        // console.log(weekNumber, eventTime);
    
        leagueName = weekNumber = weekNumber.replace('League ID ', '').trim();
        let panelsInner = pn.querySelectorAll('.collapsed, .expanded');
        let togglePanel = (element) => {
            if (element.classList.contains('collapsed')) 
                element.childNodes[0].click();
        };
        togglePanel(pn.childNodes[0]);
        panelsInner.forEach((panel) => {
            panel.querySelectorAll('.grid').forEach((game) => {
                const team1 = game.querySelector('.team-name:nth-child(1)')?.textContent.trim();
                const team2 = game.querySelector('.team-name:nth-child(3)')?.textContent.trim();
                const score = game.querySelector('.scoreboard-content')?.textContent.trim();
    
                let [team1Goals, team2Goals] = score.split('-').map(Number);
    
                let clubNames = ['ARS', 'CHE', 'MCI', 'MUN', 'LIV', 'TOT'];
                if (clubNames.includes(team1) || clubNames.includes(team2)) {
                    console.log(weekNumber, team1, score, team2);
                    const gameId = leagueName.split(' ')[0];
                    resultsAll.push({ weekNumber, team1, score, team2, gameId });
                    //if (team1Goals + team2Goals < 2) {
                    //    panel.querySelector('.grid.grid-middle.title-center.ng-star-inserted').style.backgroundColor = '#43e569';
                    //} else {
                    //    panel.querySelector('.grid.grid-middle.title-center.ng-star-inserted').style.backgroundColor = 'red';
                    //}
                }
            });
        });    
    });
    //resultsAll.sort((a, b) => a.gameId - b.gameId);
    resultsAll.reverse();
    console.log({ AllResults: resultsAll, LeagueName: leagueName });
    return { AllResults: resultsAll, LeagueName: leagueName };
})();

