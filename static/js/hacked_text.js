const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

        // Add event listeners to all <a> elements inside <li> elements
        document.querySelectorAll("li > a").forEach(link => {
            // Initialize interval variable for each link
            let interval = null;

            // Add mouseover event listener to each link
            link.addEventListener('mouseover', event => {
                let iteration = 0;

                // Clear any existing intervals to prevent multiple animations
                clearInterval(interval);

                // Start a new interval for the animation
                interval = setInterval(() => {
                    // Modify the text content of the link during each iteration
                    event.target.innerText = event.target.innerText
                        .split("")
                        .map((letter, index) => {
                            // Replace letters with corresponding letters from dataset value
                            if (index < iteration) {
                                return event.target.dataset.value[index];
                            }

                            // Randomly select letters if animation is still ongoing
                            return letters[Math.floor(Math.random() * 26)];
                        })
                        .join("");

                    // Stop the animation when all letters have been replaced
                    if (iteration >= event.target.dataset.value.length) {
                        clearInterval(interval);
                    }

                    // Increment the iteration counter for smoother animation
                    iteration += 1 / 3;
                }, 40);
            });
        });