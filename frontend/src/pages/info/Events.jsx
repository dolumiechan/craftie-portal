import InfoPage from '../../components/layout/InfoPage';
import EmptyState from '../../components/ui/EmptyState';

export default function Events() {
  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <InfoPage title="Мероприятия">
        <p>
          Здесь будут офлайн-встречи мастер-классов и ярмарки ремёсел. Раздел подключится к
          мероприятиям в следующей версии.
        </p>
      </InfoPage>
      <EmptyState
        title="Расписание пока пусто"
        description="Следите за обновлениями. Анонсы появятся в этом разделе."
      />
    </div>
  );
}
