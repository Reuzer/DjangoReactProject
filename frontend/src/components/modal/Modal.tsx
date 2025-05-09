import React, { ReactNode, useEffect } from "react";
import styles from "./Modal.module.css"; // Подключаем CSS-модуль (альтернатива — styled-components или inline-стили)

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  children: ReactNode;
  closeOnOutsideClick?: boolean; // Закрывать при клике вне модалки? (по умолчанию true)
}

export const Modal = ({
  isOpen,
  onClose,
  children,
  closeOnOutsideClick = true,
}: ModalProps) => {
  // Закрытие модалки по Escape
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };

    if (isOpen) {
      document.addEventListener("keydown", handleKeyDown);
    }

    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className={styles.modalOverlay}>
      <div
        className={styles.modalContent}
        onClick={(e) => e.stopPropagation()} // Предотвращаем закрытие при клике внутри модалки
      >
        <button className={styles.closeButton} onClick={onClose}>
          &times;
        </button>
        {children}
      </div>
    </div>
  );
};