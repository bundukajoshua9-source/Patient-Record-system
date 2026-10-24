"""
Patient Record System
Digital Public Good (DPG) aligned: open-source, privacy-respecting
(no address, phone number or detailed medical history stored),
modular and reusable.
"""

# Tuple (optional extra marks): fixed list of visit types
VISIT_TYPES = ("Checkup", "Vaccination", "Follow-up", "Emergency")


class Visit:
    """Records one visit made by a patient."""

    def __init__(self, visit_type, reason, temperature):
        self.visit_type = visit_type
        self.reason = reason
        self.temperature = temperature
        self.fever_status = Visit.check_fever(temperature)

    @staticmethod
    def check_fever(temperature):
        """Static method: needs no class or instance data."""
        if temperature >= 38.0:
            return "Fever"
        elif temperature < 35.0:
            return "Low temperature"
        return "Normal"

    def display_visit(self):
        print(f"   {self.visit_type:<12} | Reason: {self.reason:<18} "
              f"| Temp: {self.temperature}C ({self.fever_status})")


class Patient:
    """A patient identified by an anonymous ID (privacy-respecting)."""

    total_patients = 0  # class attribute

    def __init__(self, patient_id, first_name, age):
        self.patient_id = patient_id
        self.first_name = first_name
        self.age = age
        self.visits = []  # list of Visit objects
        Patient.total_patients += 1

    # ---------- Instance methods ----------
    def add_visit(self, visit_type, reason, temperature):
        if visit_type not in VISIT_TYPES:
            print(f"Invalid visit type. Choose from: {', '.join(VISIT_TYPES)}")
            return
        if not 30 <= temperature <= 45:
            print("Temperature must be between 30 and 45 C.")
            return
        self.visits.append(Visit(visit_type, reason, temperature))
        print(f"Visit recorded for {self.first_name}.")

    def update_record(self, new_age):
        self.age = new_age
        print(f"Age updated for {self.first_name}.")

    def display_info(self):
        print(f"\nID: {self.patient_id} | Name: {self.first_name} | Age: {self.age}")
        if not self.visits:
            print("   No visits recorded yet.")
        for visit in self.visits:
            visit.display_visit()

    # ---------- Class method ----------
    @classmethod
    def get_total_patients(cls):
        return cls.total_patients


# ---------- Data structure: dictionary (ID -> Patient object) ----------
patients = {}


def add_patient(patient_id, first_name, age):
    if patient_id in patients:
        print("A patient with this ID already exists.")
        return
    patients[patient_id] = Patient(patient_id, first_name, age)
    print(f"Patient {first_name} added.")


def display_all_patients():
    if not patients:
        print("No patients recorded yet.")
        return
    for patient in patients.values():
        patient.display_info()
    print(f"\nTotal patients: {Patient.get_total_patients()}")


def main():
    while True:
        print("\n=== Patient Record System ===")
        print("1. Add patient")
        print("2. Record a visit")
        print("3. Update patient age")
        print("4. Display all patients")
        print("5. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            pid = input("Patient ID (e.g. PAT001): ").strip().upper()
            name = input("First name: ").strip()
            try:
                age = int(input("Age: "))
            except ValueError:
                print("Please enter a valid number.")
                continue
            add_patient(pid, name, age)

        elif choice == "2":
            pid = input("Patient ID: ").strip().upper()
            if pid not in patients:
                print("Patient not found.")
                continue
            print("Visit types:", ", ".join(VISIT_TYPES))
            visit_type = input("Visit type: ").strip().title()
            reason = input("Reason (short): ").strip()
            try:
                temp = float(input("Temperature in C: "))
            except ValueError:
                print("Please enter a valid number.")
                continue
            patients[pid].add_visit(visit_type, reason, temp)

        elif choice == "3":
            pid = input("Patient ID: ").strip().upper()
            if pid not in patients:
                print("Patient not found.")
                continue
            try:
                new_age = int(input("New age: "))
            except ValueError:
                print("Please enter a valid number.")
                continue
            patients[pid].update_record(new_age)

        elif choice == "4":
            display_all_patients()

        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()