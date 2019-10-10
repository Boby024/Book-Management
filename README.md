# Book-Management
Realisierung einer Bücherverwaltung : (Frontend: Angular and Backend: Python, Flask {api} )
*volle Version ,on the branch: fullversion

Aufgabenstellung 
Im Rahmen dieser Übungsaufgabe solle ich eine Webanwendung erstellen, die eine Bücherverwaltung realisiert. Benutzer sollen sich an einem Online-System anmelden und über eine Weboberfläche einen Bücherkatalog einsehen, verwalten sowie Bücher ausleihen können. Darüber hinaus soll das System eine geeignete REST-Schnittstelle zur Verfügung stellen, die ebenfalls einige dieser Funktionen anbietet.
Eine Umsetzung dieser Anwendung erfordert sowohl eine Backend- als auch eine FrontendImplementierung. Darüber hinaus ist eine Datenbankanbindung erforderlich, damit die Daten persistent gespeichert werden können.

Fachliche Anforderungen 
Das System soll drei wesentliche Komponenten umfassen: Eine Benutzerverwaltung, eine Weboberfläche zur Verwaltung der Bücher sowie eine entsprechende REST-Schnittstelle. Die Anforderungen an diese Komponenten sind im Folgenden beschrieben:

Benutzerverwaltung 
Benutzer sollen sich auf der Webseite zunächst mit ihrer E-Mail-Adresse und einem frei wählbaren Passwort registrieren können. Später können sie sich am System mit ihrer E-MailAdresse und ihrem gewählten Passwort einloggen. Ein erfolgreicher Login ist für die Nutzung der Weboberfläche zur Verwaltung der Bücher erforderlich.

Weboberfläche zur Verwaltung der Bücher 
Über die Weboberfläche sollen eingeloggte Benutzer den Bücherkatalog einsehen, verwalten sowie Bücher ausleihen können. Folgende Funktionen sollen zur Verfügung stehen:
• Buch hinzufügen – Benutzer können ein neues Buch zum Bücherkatalog hinzufügen. Hierzu müssen sie für jedes hinzuzufügende Buch die folgenden Angaben hinterlegen: 
           o Titel – Der Titel des Buchs 
           o Autor(en) – Der bzw. die Autor(en) des Buchs 
           o Verlag – Der Verlag, in dem das Buch erschienen ist 
           o Erscheinungsjahr – Das Jahr, in dem das Buch erschienen ist
• Buch entfernen – Benutzer können ein vorhandenes Buch aus dem Katalog des Systems entfernen. 
• Buch ausleihen – Benutzer können ein Buch, welches nicht bereits verliehen wurde, für eine unbestimmte Zeitdauer ausleihen. Das Buch wird daraufhin entsprechend als von diesem Benutzer ausgeliehen markiert. Jeder Benutzer darf maximal drei Bücher zur gleichen Zeit ausleihen.
• Buch zurückgeben – Benutzer, die zuvor ein Buch ausgeliehen haben, können dieses über das Online-System auch wieder zurückgeben. Diese Aktion kann nur von demjenigen Benutzer ausgeführt werden, der das entsprechende Buch zuvor ausgeliehen hat.
• Bücherkatalog einsehen – Jeder Benutzer kann jederzeit eine Übersicht über alle Bücher im Katalog anzeigen lassen. Die Übersicht stellt zum einen die Merkmale (Titel, Autor(en), Verlag, Erscheinungsjahr) jedes Buchs dar. Zum anderen ist für jedes Buch ersichtlich, ob es aktuell verfügbar oder verliehen ist. Falls ein Buch aktuell verliehen ist, wird darüber hinaus angezeigt, welcher Benutzer dieses Buch derzeit besitzt und wann er es ausgeliehen hat.

REST-Schnittstelle zur Verwaltung der Bücher 
Die folgenden Operationen sollen ebenfalls über eine geeignete REST-Schnittstelle ausführbar sein:
• Buch hinzufügen 
• Buch entfernen 
• Bücherkatalog abrufen (als JSON)
