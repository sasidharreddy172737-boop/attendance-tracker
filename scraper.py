import json
import os
import datetime


class subject:
    def __init__(self, subject_name, total_classes):
        self.sub = subject_name
        self.total_class = total_classes
        self.history = []

    def mark_attendance(self, status):
        date = str(datetime.date.today())
        self.history.append({"STATUS": status, "DATE": date})

    def notheld_classes(self):
        return sum(1 for h in self.history if h["STATUS"] == "N")

    def present_classes(self):
        return sum(1 for h in self.history if h["STATUS"] == "P")

    def absent_classes(self):
        return sum(1 for h in self.history if h["STATUS"] == "A")

    def remaining_classes(self):
        return self.total_class - len(self.history)

    def current_attendance(self):
        ab = self.absent_classes()
        pr = self.present_classes()
        held = ab + pr
        if held == 0:
            return 0
        return (pr / held) * 100

    def max_skip_classes(self):
        presentc = self.present_classes()
        remainingc = self.remaining_classes()
        max_skip = (remainingc + presentc) - (0.75 * self.total_class)
        return max(0, int(max_skip))

    def min_attend_classes(self):
        presentc = self.present_classes()
        remaining = self.remaining_classes()
        need = (0.75 * self.total_class) - presentc
        if need <= 0:
            return 0
        need = int(need) + 1 if need > int(need) else int(need)
        return min(need, remaining)

    def get_status_message(self):
        pct = self.current_attendance()
        if pct >= 75:
            skip = self.max_skip_classes()
            return f"SAFE-CAN SKIP {skip} MORE CLASSES"
        else:
            attend = self.min_attend_classes()
            return f"WARNING-MUST ATTEND ALL {attend} CLASSES"

    def to_dict(self):
        return {
            "name": self.sub,
            "total_classes": self.total_class,
            "history": self.history
        }

    @classmethod
    def from_dict(cls, data):
        s = cls(data["name"], data["total_classes"])
        s.history = data["history"]
        return s


class semester:
    def __init__(self, name):
        self.name = name
        self.subj = {}

    def add_subject(self, name, total_cla):
        self.subj[name] = subject(name, total_cla)

    def mark_subject(self, subject_name, status):
        if subject_name in self.subj:
            self.subj[subject_name].mark_attendance(status)
        else:
            print("SUBJECT NOT FOUND")

    

    def to_dict1(self):
        return {
            "name": self.name,
            "subjects": {name: s.to_dict() for name, s in self.subj.items()}
        }

    @classmethod
    def from_dict1(cls, data1):
        sem = cls(data1["name"])
        for name, sub_data in data1["subjects"].items():
            sem.subj[name] = subject.from_dict(sub_data)
        return sem


class attendance:
    def __init__(self, file):
        self.file = file
        self.Sem = {}
        self.load_data()

    def add_sem(self, name):
        if name not in self.Sem:
            self.Sem[name] = semester(name)
            self.save_data()

    def save_data(self):
        data = {name: sem.to_dict1() for name, sem in self.Sem.items()}
        with open(self.file, "w") as f:
            json.dump(data, f, indent=2)

    def load_data(self):
        if os.path.exists(self.file):
            try:
                with open(self.file, "r") as f:
                    content = f.read().strip()
                    if content == "":
                        return
                    data = json.loads(content)
                for name, sem_data in data.items():
                    self.Sem[name] = semester.from_dict1(sem_data)
            except json.JSONDecodeError:
                print("Attendance file was empty or corrupted — starting fresh")