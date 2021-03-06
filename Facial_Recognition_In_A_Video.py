import cv2
import pyodbc
import face_recognition

video_capture = cv2.VideoCapture("Video_File_Name")

connection_string = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=server_name; DATABASE=database_name; UID=user_name; PWD=password')

mycursor = connection_string.cursor()

mycursor.execute("select * from Users")
rows = mycursor.fetchall()

known_face_names=[]
known_face_encodings =[]
for r in rows:
    known_face_encodings.append(face_recognition.face_encodings(face_recognition.load_image_file(r[1]))[0])
    known_face_names.append(r[0])

while True:
    ret, frame = video_capture.read()
    rgb_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Random Person"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 1)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        if (name != "Random Person"):
            print(name, "was here")

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
