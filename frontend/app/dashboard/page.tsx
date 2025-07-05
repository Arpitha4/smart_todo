"use client";

import { useEffect, useState } from "react";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { Textarea } from "../../components/ui/textarea";
import { Dialog } from "@headlessui/react";
import { X, Pencil } from "lucide-react";

interface Task {
  id: number;
  title: string;
  description?: string;
  priority: string;
  category: string;
  status: string;
  deadline?: string;
  completed?: boolean;
}

const BASE_URL = "http://127.0.0.1:8000/api";

const PRIORITIES = ["High", "Medium", "Low"];
const CATEGORIES = ["Frontend", "Backend"];
const STATUSES = ["Pending", "Started", "Completed"];



function getPriorityColor(priority: string): string {
  switch (priority.toLowerCase()) {
    case "high": return "text-red-600";
    case "medium": return "text-yellow-500";
    case "low": return "text-green-600";
    default: return "text-gray-600";
  }
}

export default function Dashboard() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [prevStatus, setPrevStatus] = useState<string>("");
  const [editTask, setEditTask] = useState<Task | null>(null);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [newTask, setNewTask] = useState({
    title: "",
    description: "",
    priority: "Medium",
    deadline: "",
    completed: false,
    category: "",
    status: "Pending",
  });
  const [filter, setFilter] = useState({ category: "", status: "", priority: "" });

  useEffect(() => {
    fetch(`${BASE_URL}/tasks/`)
      .then(res => res.json())
      .then(setTasks);
  }, []);

  const openEditModal = (task: Task) => {
    setEditTask({ ...task });
    setIsEditModalOpen(true);
  };

  const saveEditedTask = async () => {
    if (!editTask) return;
    const response = await fetch(`${BASE_URL}/tasks/${editTask.id}/`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(editTask),
    });
    if (response.ok) {
      const updated = await response.json();
      setTasks(prev => prev.map(t => (t.id === updated.id ? updated : t)));
      setIsEditModalOpen(false);
    } else {
      alert("Failed to update task");
    }
  };

  const addTask = async () => {
    const response = await fetch(`${BASE_URL}/tasks/create/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newTask),
    });
    if (response.ok) {
      const newItem = await response.json();
      setTasks(prev => [...prev, newItem]);
      setNewTask({
        title: "",
        description: "",
        priority: "",
        deadline: "",
        completed: false,
        category: "",
        status: "",
      });
      setIsAddModalOpen(false);
    } else {
      alert("Failed to add task");
    }
  };

  const filteredTasks = tasks.filter(task => {
    const matchesCategory = !filter.category || task.category === filter.category;
    const matchesStatus = !filter.status || task.status === filter.status;
    const matchesPriority = !filter.priority || task.priority === filter.priority;
    return matchesCategory && matchesStatus && matchesPriority;
  });

  return (
    <main className="p-8 max-w-7xl mx-auto space-y-10">
      <h1 className="text-3xl font-bold text-indigo-700">Task Dashboard</h1>

      <div className="flex justify-between items-center">
        <div className="flex flex-wrap gap-4">
          <select
            value={filter.category}
            onChange={e => setFilter({ ...filter, category: e.target.value })}
            className="border rounded px-3 py-2"
          >
            <option value="">All Category</option>
            {CATEGORIES.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
          <select
            value={filter.status}
            onChange={e => setFilter({ ...filter, status: e.target.value })}
            className="border rounded px-3 py-2"
          >
            <option value="">All Status</option>
            {STATUSES.map(stat => (
              <option key={stat} value={stat}>{stat}</option>
            ))}
          </select>
          <select
            value={filter.priority}
            onChange={e => setFilter({ ...filter, priority: e.target.value })}
            className="border rounded px-3 py-2"
          >
            <option value="">All Priority</option>
            {PRIORITIES.map(p => (
              <option key={p} value={p}>{p}</option>
            ))}
          </select>
        </div>
        <Button onClick={() => setIsAddModalOpen(true)}>+ Add Task</Button>
      </div>

      <div className="overflow-auto">
        <table className="min-w-full table-fixed divide-y divide-gray-200 border text-sm">
          <thead className="bg-gray-100">
            <tr>
              <th className="px-4 py-2 text-left">Title</th>
              <th className="px-4 py-2 text-left">Description</th>
              <th className="px-4 py-2 text-left">Priority</th>
              <th className="px-4 py-2 text-left">Deadline</th>
              <th className="px-4 py-2 text-left">Completed</th>
              <th className="px-4 py-2 text-left">Category</th>
              <th className="px-4 py-2 text-left">Status</th>
              <th className="px-4 py-2 text-left">Action</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {filteredTasks.map(task => (
              <tr key={task.id}>
                <td className="px-4 py-2 font-medium">{task.title}</td>
                <td className="px-4 py-2">{task.description}</td>
                <td className={`px-4 py-2 font-semibold ${getPriorityColor(task.priority)}`}>{task.priority}</td>
                <td className="px-4 py-2">{task.deadline}</td>
                <td className="px-4 py-2">
                  <input type="checkbox" checked={task.completed} readOnly />
                </td>
                <td className="px-4 py-2">{task.category}</td>
                <td className="px-4 py-2">{task.status}</td>
                <td className="px-4 py-2">
                  <span
                    onClick={() => openEditModal(task)}
                    className="text-indigo-600 hover:underline cursor-pointer"
                  >
                    <Pencil className="w-4 h-4 inline" />
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <Dialog open={isAddModalOpen} onClose={() => setIsAddModalOpen(false)} className="relative z-50">
        <div className="fixed inset-0 bg-black/30" aria-hidden="true" />
        <div className="fixed inset-0 flex items-center justify-center p-4">
          <Dialog.Panel className="mx-auto w-full max-w-lg rounded-xl bg-white p-6 shadow-lg space-y-4">
            <div className="flex justify-between items-center mb-2">
              <Dialog.Title className="text-xl font-bold">Add New Task</Dialog.Title>
              <button onClick={() => setIsAddModalOpen(false)} className="text-gray-400 hover:text-black">
                <X className="w-5 h-5" />
              </button>
            </div>
            <div className="grid md:grid-cols-2 gap-4">
              <Input
                value={newTask.title}
                onChange={e => setNewTask({ ...newTask, title: e.target.value })}
                placeholder="Task Title"
              />
              <select
                value={newTask.priority}
                onChange={e => setNewTask({ ...newTask, priority: e.target.value })}
                className="border rounded px-3 py-2"
              >
                <option value="">Select Priority</option>
                {PRIORITIES.map(p => (
                  <option key={p} value={p}>{p}</option>
                ))}
              </select>
              <Input
                type="date"
                value={newTask.deadline}
                min={new Date().toISOString().split("T")[0]}
                onChange={e => setNewTask({ ...newTask, deadline: e.target.value })}
              />
              <select
                value={newTask.category}
                onChange={e => setNewTask({ ...newTask, category: e.target.value })}
                className="border rounded px-3 py-2"
              >
                <option value="">Select Category</option>
                {CATEGORIES.map(cat => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
              <Textarea
                value={newTask.description}
                onChange={e => setNewTask({ ...newTask, description: e.target.value })}
                placeholder="Description"
                className="col-span-2"
              />
<select
  value={newTask.status}
  onChange={e => setNewTask({ ...newTask, status: e.target.value })}
  disabled={newTask.completed}
  className="border rounded px-3 py-2 col-span-2"
>
  <option value="">Select Status</option>
  {STATUSES.map(stat => (
    <option key={stat} value={stat}>
      {stat}
    </option>
  ))}
</select>
              <label className="flex items-center gap-2 col-span-2">
  <input
    type="checkbox"
    checked={newTask.completed}
    onChange={e => {
      const isChecked = e.target.checked;
      setNewTask({
        ...newTask,
        completed: isChecked,
        status: isChecked ? "Completed" : "", // or revert to previous status if needed
      });
    }}
  />
  Mark as Completed
</label>
            </div>
            <div className="flex justify-end">
              <Button onClick={addTask}>Add Task</Button>
            </div>
          </Dialog.Panel>
        </div>
      </Dialog>

      <Dialog open={isEditModalOpen} onClose={() => setIsEditModalOpen(false)} className="relative z-50">
        <div className="fixed inset-0 bg-black/30" aria-hidden="true" />
        <div className="fixed inset-0 flex items-center justify-center p-4">
          <Dialog.Panel className="mx-auto w-full max-w-lg rounded-xl bg-white p-6 shadow-lg space-y-4">
            <div className="flex justify-between items-center mb-2">
              <Dialog.Title className="text-xl font-bold">Edit Task</Dialog.Title>
              <button onClick={() => setIsEditModalOpen(false)} className="text-gray-400 hover:text-black">
                <X className="w-5 h-5" />
              </button>
            </div>
            {editTask && (
  <div className="grid md:grid-cols-2 gap-4">
    {/* Title - DISABLED while editing */}
    <Input
      value={editTask.title}
      onChange={e => setEditTask({ ...editTask, title: e.target.value })}
      placeholder="Task Title"
      disabled
    />

    {/* Priority - DISABLED while editing */}
    <select
      value={editTask.priority}
      onChange={e => setEditTask({ ...editTask, priority: e.target.value })}
      className="border rounded px-3 py-2"
      disabled
    >
      <option value="">Select Priority</option>
      {PRIORITIES.map(p => (
        <option key={p} value={p}>{p}</option>
      ))}
    </select>

    {/* Deadline - DISABLED while editing */}
    <Input
      type="date"
      value={editTask.deadline?.slice(0, 10)}
      min={new Date().toISOString().split("T")[0]}
      onChange={e => setEditTask({ ...editTask, deadline: e.target.value })}
      disabled
    />

    {/* Category - editable */}
    <select
      value={editTask.category}
      onChange={e => setEditTask({ ...editTask, category: e.target.value })}
      className="border rounded px-3 py-2"
    >
      <option value="">Select Category</option>
      {CATEGORIES.map(cat => (
        <option key={cat} value={cat}>{cat}</option>
      ))}
    </select>

    {/* Description - editable */}
    <Textarea
      value={editTask.description}
      onChange={e => setEditTask({ ...editTask, description: e.target.value })}
      placeholder="Description"
      className="col-span-2"
    />

    {/* Status - auto-select "Completed" if checkbox is ticked */}
<select
  value={editTask.status}
  onChange={e => setEditTask({ ...editTask, status: e.target.value })}
  disabled={editTask.completed}
  className="border rounded px-3 py-2 col-span-2"
>
  <option value="">Select Status</option>
  {STATUSES.map(stat => (
    <option key={stat} value={stat}>{stat}</option>
  ))}
</select>


    {/* Completed Checkbox */}
    <label className="flex items-center gap-2 col-span-2">
<input
  type="checkbox"
  checked={editTask.completed}
  onChange={e => {
    const isChecked = e.target.checked;

    setEditTask(prev => ({
      ...prev,
      completed: isChecked,
      status: isChecked
        ? "Completed"
        : prevStatus || "Pending", // restore or fallback
    }));

    if (!isChecked) {
      setPrevStatus(""); // reset previous
    } else {
      setPrevStatus(editTask.status); // save current before overriding
    }
  }}
/>
      Mark as Completed
    </label>
  </div>
)}
            <div className="flex justify-end">
              <Button onClick={saveEditedTask}>Save Changes</Button>
            </div>
          </Dialog.Panel>
        </div>
      </Dialog>
    </main>
  );
}
