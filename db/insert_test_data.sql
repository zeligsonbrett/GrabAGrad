INSERT INTO
    GRADUATES (name, acad_dept, bio)
VALUES
    ('John Doe SPIA', 'Princeton School of Public and International Affairs',
    'Hi, I am John Doe, and I really like international affairs! Specifically, I study US-Russia relations.'),
    ('John Doe COS', 'Computer Science',
    'Hi, I am John Doe, and I really like computers. I am researching novel machine learning algorithms.'),
    ('John Doe PLM', 'Plasma Physics',
    'Hi, I am John Doe, and I want to make the first energy net-positive fusion reactor.'),
    ('John Doe PHI', 'Philosophy',
    'Hi, I am John Doe... Or am I? How should I know? Also, what is knowing?'),
    ('John Doe SPA', 'Spanish and Portuguese',
    'Hola, soy John Doe, y estudio la literatura hispanica.'),
    ('Jane Doe QCB', 'Quantitative and Computational Biology',
    'Hi, I am Jane Doe, and I am developing statistical models to analyze biomedical data to better understand human disease.'),
    ('Jane Doe NEU', 'Neuroscience',
    'Hi, I am Jane Doe, and I am working to image the brain!'),
    ('Jane Doe ECE', 'Electrical and Computer Engineering',
    'Hi, I am Jane Doe, and circuits make me happy'),
    ('Jane Doe MAT', 'Mathematics',
    'Hi, I am Jane Doe, and I can prove in less the 10 seconds that .9999 repeating equals 1'),
    ('Jane Doe FIN', 'Finance',
    'Hi, I am Jane Doe, and I previously worked at Jane Street.');

INSERT INTO
    GRAD_INDUSTRIES (id, industry)
VALUES
    (1, 'Government'),
    (1, 'Health Care'),
    (2, 'Information Technology'),
    (3, 'Energy'),
    (4, 'Government'),
    (5, 'Education'),
    (6, 'Pharmaceuticals'),
    (6, 'Information Technology'),
    (7, 'Government'),
    (7, 'Health Care'),
    (8, 'Information Technology'),
    (8, 'Defense'),
    (9, 'Insurance'),
    (10, 'Finance');


INSERT INTO
    GRAD_EXPERIENCES (id, experience, experience_desc)
VALUES
    (1, 'Idaho Congressional Office, Congressional Assistant', 'Suggested important policy decisions in line with representative beliefs.'),
    (1, 'J&J, Lobbyist', 'I worked to get drugs approved by the FDA'),
    (2, 'Google, Software Engineer', 'I was a backend developer for Gmail'),
    (3, 'Princeton Plasma Physics Laboratory, Researcher', 'I performed experiments to produce stable plasmas'),
    (4, 'Urban Institute, Research Fellow', ''),
    (4, 'Economic Policy Institute, Research Fellow', 'Worked to analyze economic impacts of expanding medicare access'),
    (5, 'Riverside Elementary School, Teacher', 'I taught Spanish to elementary school students.'),
    (6, 'Merck, Computational Biologist', 'I leveraged data to support drug development.'),
    (6, 'Novartis, Machine Learning Engineer', 'I developed algorithms for medical companies.'),
    (7, 'City of Houston, Safety Specialist', 'Policy advocate for keeping kids safe in high school sports.'),
    (7, 'Rice University, Research Assistant', 'Studied cognitive function in a lab.'),
    (8, 'IBM, Software Engineer', 'I was a backend developer'),
    (8, 'Lockheed Martin, Electrical Engineer', 'I worked on defense drones'),
    (9, 'Liberty Mutual, Actuary', 'I was an actuary who worked to create insurance policies'),
    (10, 'Citigroup, Financial analyst', 'Assessed stock performance.');

INSERT INTO
    GRAD_INTERESTS (id, interest)
VALUES
    (1, 'Running'),
    (2, 'Running'),
    (2, 'Singing'),
    (2, 'Mountain Biking'),
    (3, 'Cryptocurrency'),
    (4, 'Debate'),
    (5, 'Dance'),
    (6, 'Drawing'),
    (7, 'Video Games'),
    (8, 'Hiking'),
    (9, 'Photography'),
    (10, 'Gardening'),
    (10, 'Cooking');

INSERT INTO
    GRAD_CONTACT (id, email, phone)
VALUES
    (2, 'fakeemail2@gmail.com', '231-345-4567'),
    (3, 'fakeemail3@gmail.com', '312-345-4567'),
    (4, 'fakeemail4@gmail.com', '444-345-4567'),
    (5, 'fakeemail5@gmail.com', '555-345-4567');

INSERT INTO
    GRAD_CONTACT (id, phone)
VALUES
    (6, '666-345-4567'),
    (7, '777-345-4567');

INSERT INTO
    GRAD_CONTACT (id, email)
VALUES
    (8, 'fakeemail8@gmail.com'),
    (9, 'fakeemail9@gmail.com'),
    (10, 'fakeemail10@gmail.com');




