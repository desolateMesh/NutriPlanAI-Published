// frontend/src/components/PreferencesModal.tsx
import React from 'react';
import type { UserOut } from '../types';

interface PreferencesModalProps {
  profile: UserOut;
  onClose: () => void;
}

export const PreferencesModal: React.FC<PreferencesModalProps> = ({ profile, onClose }) => {
  return (
    <div 
      onClick={onClose} 
      className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-60 backdrop-blur-sm"
    >
      <div 
        onClick={(e) => e.stopPropagation()} 
        className="bg-white rounded-lg shadow-xl w-full max-w-md p-6 m-4"
      >
        <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-bold text-gray-800">⚙️ Your Preferences</h2>
            <button onClick={onClose} className="text-gray-500 hover:text-gray-800 text-3xl font-bold">&times;</button>
        </div>
        <p className="text-gray-600 mb-4">Changes to preferences will be applied the next time you generate a plan.</p>
        <div className="space-y-3">
          <label className="flex items-center text-lg">
            <input type="checkbox" className="h-5 w-5" defaultChecked={profile.preferences['vegetarian']} disabled />
            <span className="ml-3">Vegetarian</span>
          </label>
          <label className="flex items-center text-lg">
            <input type="checkbox" className="h-5 w-5" defaultChecked={profile.preferences['gluten_free']} disabled />
            <span className="ml-3">Gluten-Free</span>
          </label>
          <label className="flex items-center text-lg">
            <input type="checkbox" className="h-5 w-5" defaultChecked={profile.preferences['dairy_free']} disabled />
            <span className="ml-3">Dairy-Free</span>
          </label>
        </div>
        <button className="mt-6 w-full bg-gray-300 font-bold py-2 px-4 rounded cursor-not-allowed">
          Save Changes (Disabled)
        </button>
      </div>
    </div>
  );
};