import InfoPage from '../../components/layout/InfoPage';

export default function Contacts() {
  return (
    <InfoPage title="Контакты">
      <p>По вопросам работы портала и модерации контента:</p>
      <ul className="list-inside list-disc space-y-1">
        <li>Email: support@craft-portal.example</li>
        <li>Telegram: @craft_portal_support</li>
      </ul>
      <p className="text-craft-brown/60">Контакты указаны для демонстрационного проекта.</p>
    </InfoPage>
  );
}
