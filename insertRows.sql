-- Sample data for Reel & Frame Books
-- 5 categories, 15 books (3 per category)

PRAGMA foreign_keys = ON;

INSERT INTO category (categoryId, categoryName, categoryDescription, categoryImage) VALUES
(1, 'Film Criticism',  'Directors and critics writing about the art of cinema', 'film-criticism.jpg'),
(2, 'Screenwriting',   'Story structure and the craft of writing scripts',     'screenwriting.jpg'),
(3, 'Filmmaking',      'Practical guides to directing, editing and producing', 'filmmaking.jpg'),
(4, 'Media Theory',    'How mass media shape culture, politics and attention', 'media-theory.jpg'),
(5, 'Photography',     'Essays on images, photography and ways of looking',    'photography.jpg');

INSERT INTO book (bookId, categoryId, title, author, isbn, publishYear, price, image, readNow) VALUES
-- Film Criticism
(1,  1, 'Hitchcock (Revised Edition)', 'Francois Truffaut', '9780671604295', 1985, 25.00, 'hitchcock-truffaut.jpg', 1),
(2,  1, 'Sculpting in Time: Reflections on the Cinema', 'Andrey Tarkovsky', '9780292776241', 1989, 24.95, 'sculpting-in-time.jpg', 0),
(3,  1, 'Notes on the Cinematograph', 'Robert Bresson', '9781681370248', 2016, 15.95, 'notes-cinematograph.jpg', 0),
-- Screenwriting
(4,  2, 'Story: Substance, Structure, Style, and the Principles of Screenwriting', 'Robert McKee', '9780060391683', 1997, 45.00, 'story-mckee.jpg', 1),
(5,  2, 'Screenplay: The Foundations of Screenwriting', 'Syd Field', '9780385339032', 2005, 20.00, 'screenplay-field.jpg', 0),
(6,  2, 'Save the Cat!', 'Blake Snyder', '9781932907001', 2005, 19.95, 'save-the-cat.jpg', 1),
-- Filmmaking
(7,  3, 'Rebel Without a Crew', 'Robert Rodriguez', '9780452271876', 1996, 18.00, 'rebel-without-a-crew.jpg', 0),
(8,  3, 'In the Blink of an Eye', 'Walter Murch', '9781879505629', 2001, 14.95, 'blink-of-an-eye.jpg', 1),
(9,  3, 'Directing Actors', 'Judith Weston', '9780941188241', 1996, 26.95, 'directing-actors.jpg', 0),
-- Media Theory
(10, 4, 'Understanding Media: The Extensions of Man', 'Marshall McLuhan', '9780262631594', 1994, 35.00, 'understanding-media.jpg', 1),
(11, 4, 'Amusing Ourselves to Death', 'Neil Postman', '9780143036531', 2005, 18.00, 'amusing-ourselves.jpg', 0),
(12, 4, 'Manufacturing Consent', 'Edward S. Herman, Noam Chomsky', '9780375714498', 2002, 21.00, 'manufacturing-consent.jpg', 0),
-- Photography
(13, 5, 'On Photography', 'Susan Sontag', '9780312420093', 2001, 18.00, 'on-photography.jpg', 1),
(14, 5, 'Camera Lucida', 'Roland Barthes', '9780374532338', 2010, 17.00, 'camera-lucida.jpg', 0),
(15, 5, 'Ways of Seeing', 'John Berger', '9780140135152', 1990, 17.00, 'ways-of-seeing.jpg', 0);
